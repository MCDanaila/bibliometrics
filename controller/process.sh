#!/bin/bash

this_dir=$(dirname $0)
root_dir=$( echo $this_dir | sed 's/controller.*//')
db_dir=${root_dir}db
controller_dir=${root_dir}controller
lib_dir=${root_dir}libbiblio

provider=$1
source_dir=$2
work_dir=$3
update_refresh=$4

if [ $# -lt 4 ]
then
  echo "Refresh or update requirement must be stated"
  exit -1
fi

if [ $update_refresh == "update" ]
then
  echo "Data will be updated, not refreshed"
elif [ $update_refresh == "refresh" ]
then
  echo "Data will be refreshed not updated"
else
  "Update or refresh has to be specified as either update or refresh"
  exit -1
fi

db_dir=${controller_dir//controller/db}
. $db_dir/set_biblio_db_envs.sh

# Note that in updates we don't want to recreate all the tables. Main tables will be truncated 
# during the staging process, but we want staging tables updated

$controller_dir/clean_env.sh $work_dir

echo -n "Processing [$source_dir] using [$work_dir] as working area, started at " ; date

if [ $update_refresh == "update" ]
then
  $controller_dir/prepare_update.sh $provider $source_dir $work_dir $db_dir
  source_dir=$work_dir/updates    # Extracted files placed here
else
  $db_dir/$provider/RecreateAllStagingTables.sh
fi

bcp_dir=$work_dir/bcp

$controller_dir/load_daemon.sh $provider $bcp_dir ALL DUMMY_TABLE $update_refresh &
global_daemon_pid=$!

parallel_no=$(nproc)

# This needs to be revisited to stop multiple runs overwriting - AMB 24.02.24

psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "DELETE FROM \"BibliometricsFileStatus\" \
                      WHERE provider = '$provider';"
                      # WHERE (file_name = 'all_files_done' OR status IN ( 'processing', 'unprocessed') ) AND provider = '$provider';"

while [ $parallel_no -gt 0 ]
do
  echo "Launching python script"
  poetry run python3.8 $lib_dir/ingest_data.py $provider $bcp_dir &
  let "parallel_no--"
done

# This should be "write to file then copy"

for path in $source_dir/*zip
do
  file=$(basename $path)
  echo "Path found is [$path]"
  echo "File found is [$file]"
  # Need to cope with multiple zips for the same year
  year_found=$(echo $file | sed 's/_.*/_/')
  available_files=$(ls -1 ${source_dir}/${year_found}* | wc -l)
  already_there=0
  if [ $available_files -gt 1 ]
  then 
    file=${year_found}*.zip
    path=$source_dir/$file
    already_there=$(psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "SELECT FROM \"BibliometricsFileStatus\" WHERE file_name = '$file';" | grep "row" | sed 's/(//'  | cut -c1)
  fi
  if [ $already_there -eq 0 ]
  then
    psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "INSERT INTO \"BibliometricsFileStatus\" VALUES ('$file', '$path', '$provider', 'unprocessed');" 1>/dev/null
  fi
done

psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "INSERT INTO \"BibliometricsFileStatus\" VALUES ('all_files_done', '', '$provider', '');"

more_to_do=$( psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -t \
    -c "SELECT COUNT(*) FROM \"BibliometricsFileStatus\" WHERE provider = '$provider' AND status IN ( 'unprocessed', 'processing');" | sed 's/ *//g')

while [ $more_to_do -ne 0 ]
do
  wait -n

  more_to_do=$( psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -t \
    -c "SELECT COUNT(*) FROM \"BibliometricsFileStatus\" WHERE provider = '$provider' AND status IN ( 'unprocessed', 'processing');" | sed 's/ *//g')

  if [ $more_to_do -ne 0 ]
  then
    files_not_started=$( psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -t \
      -c "SELECT COUNT(*) FROM \"BibliometricsFileStatus\" WHERE provider = '$provider' AND status IN ( 'unprocessed');" | sed 's/ *//g')

    if [ $files_not_started -gt 0 ]
    then
      running_procs=$(ps --ppid $$ -lf | egrep "python|poetry" | fgrep ingest_data.py | wc -l)

      while [ $running_procs -lt $(nproc) ]
      do
        poetry run python3.8 $lib_dir/ingest_data.py $provider $bcp_dir &

        running_procs=$(ps --ppid $$ -lf | egrep "python|poetry" | fgrep ingest_data.py | wc -l)
      done
    fi
  fi
done

$controller_dir/load_daemon.sh $provider $bcp_dir MARK_COMPLETE  # Flag the system that all is done in ingestion

wait $global_daemon_pid   # Wait for the DB population to finish

echo -n "Processing [$source_dir] using [$work_dir] as working area, ended processing at " ; date

$db_dir/$provider/ProcessAllStaging.sh

echo -n "Processing [$source_dir] using [$work_dir] as working area, finished staging processing at " ; date

$db_dir/$provider/CreateAllIndexes.sh

echo -n "Processing [$source_dir] using [$work_dir] as working area, finished index creation at " ; date
