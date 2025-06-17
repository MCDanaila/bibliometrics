#!/bin/bash

provider=$1
source_dir=$2
work_dir=$3

# THERE HAS TO BE SWITCHING ON provider in this. AMB 02.01.24

echo "Processing updates from [$provider] with data in [$source_dir] and using [$work_dir] as working area"

if [[ ! -d $source_dir ]]
then
  echo "$source_dir is not a directory"
  exit -1
fi

if [[ ! -d $work_dir ]]
then
  echo "$work_dir is not a directory"
  exit -1
fi

work_dir="$work_dir/updates"

if [[ ! -d $work_dir ]]
then
  mkdir $work_dir
fi

# There should be a switch here according to the provider.... Or maybe two different scripts? AMB 21.12.24

# Get the delete files and coalesce. This code assumed the data files are like:

: <<'FILEDEF'
WOS,001133612300001,Y
WOS,001346126700001,Y
WOS,001346127800001,Y
WOS,001346127800002,Y
WOS,001346126200001,Y
WOS,001346125900001,Y
WOS,001346125700001,Y
WOS,001346244600001,Y
WOS,001346244600002,Y
WOS,001346244800001,Y
FILEDEF

deletions_file=$work_dir/deletes_list.bcp

zcat $source_dir/*.del.gz | awk -F ',' '{printf( "%s:%s\n", $1, $2)}' > $deletions_file

psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "DROP TABLE IF EXISTS temp_delete_details_$$;"
psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "CREATE TABLE temp_delete_details_$$( wos_id VARCHAR);"
psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "\COPY temp_delete_details_$$ FROM '$deletions_file';"
psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "CREATE INDEX temp_delete_idx_$$ ON \"WoSTestPublicationStaging\" (wos_id);"
psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "ANALYZE \"WoSTestPublicationStaging\";"
psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "DELETE FROM \"WoSTestPublicationStaging\" p USING temp_delete_details_$$ d WHERE p.wos_id = d.wos_id" ;
psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "DROP INDEX temp_delete_idx_$$;"
psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "DROP TABLE temp_delete_details_$$;"

# Now need to get all the tar files. No idea why WoS supply updates in this format

for path in $source_dir/*tar* 
do
  echo "Path is $path" ; 
  file=$(echo $path | awk -F'/' '{print $NF}')
  echo "File is $file"
  zip_id=$work_dir/$(echo $file | sed 's/\..*//')
  echo "zip_id is $zip_id"
  # echo "Will be doing [tar -xvzf $path -C $work_dir && zip -j -r $zip_id $zip_id]"
  tar -xvzf $path -C $work_dir && zip -j -r $zip_id $zip_id && rm -rf $zip_id
done
