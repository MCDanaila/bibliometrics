#!/bin/bash

# Remove any trailing "/". Not essential, but makes output neater
supplier=$1
bcp_dir=${2%/}
type=$3
table=$4
if [ $# -gt 4 ]
then
  update=$5
fi

echo "Start load_daemon for supplier [$supplier] bcp_dir [$bcp_dir] type [$type] table [$table]. Update is [$update]"

if [[ ! -d $bcp_dir ]]
then
  echo "$bcp_dir is not a directory"
  exit -1
fi

controller_dir=$(dirname $0)
db_dir=${controller_dir//controller/db}


# Simpler to handle both types here - avoid passing variables back and forth

if [[ $supplier == "scopus" ]]
then
  # Write this properly for scopus

  case $type in
    "ALL")
      $controller_dir/load_daemon.sh scopus $bcp_dir affiliation   ScopusTestAffiliationStaging &
      sleep 10 # So that the welcome messages don't get mixed up
      $controller_dir/load_daemon.sh scopus $bcp_dir author        ScopusTestAuthorStaging      &
      sleep 10
      $controller_dir/load_daemon.sh scopus $bcp_dir authorship    ScopusTestAuthorshipStaging  &
      sleep 10
      $controller_dir/load_daemon.sh scopus $bcp_dir source        ScopusTestSourceStaging      &
      sleep 10
      $controller_dir/load_daemon.sh scopus $bcp_dir publication   ScopusTestPublication        &
      sleep 10
      $controller_dir/load_daemon.sh scopus $bcp_dir citation      ScopusTestCitation           &
      sleep 10
      $controller_dir/load_daemon.sh scopus $bcp_dir authorkeyword ScopusTestAuthorKeyword      &
      sleep 10
      $controller_dir/load_daemon.sh scopus $bcp_dir descriptor    ScopusTestDescriptor         &
  
      wait # For them all to finish

      exit 0
      ;;
    "MARK_COMPLETE")
      $db_dir/scopus/PrepareForImport.sh $bcp_dir/complete.
      exit 0
      ;;
    "affiliation" | "author" | "source" )
      bcp_needs_sorting=1
      ;;
    *)
      bcp_needs_sorting=0
      ;;
  esac
else
  case $type in
    "ALL")
      $controller_dir/load_daemon.sh wos $bcp_dir publication WoSTestPublicationStaging $update &  # Only pub needs this
      sleep 10 # So that the welcome messages don't get mixed up

      $controller_dir/load_daemon.sh wos $bcp_dir affiliation      WoSTestAffiliationStaging      &
      sleep 10
      $controller_dir/load_daemon.sh wos $bcp_dir author           WoSTestAuthorStaging           &
      sleep 10
      $controller_dir/load_daemon.sh wos $bcp_dir authorship       WoSTestAuthorshipStaging       &
      sleep 10
      $controller_dir/load_daemon.sh wos $bcp_dir source           WoSTestSourceStaging           &
      sleep 10
      $controller_dir/load_daemon.sh wos $bcp_dir authorkeyword    WoSTestAuthorKeywordStaging    &
      sleep 10
      $controller_dir/load_daemon.sh wos $bcp_dir citation         WoSTestCitationStaging         &
      sleep 10
      $controller_dir/load_daemon.sh wos $bcp_dir grant            WoSTestGrantStaging            &
      sleep 10
      $controller_dir/load_daemon.sh wos $bcp_dir publicationgrant WoSTestPublicationGrantStaging &
      sleep 10
      $controller_dir/load_daemon.sh wos $bcp_dir puborg           WoSTestPubOrgStaging           &
      sleep 10
      $controller_dir/load_daemon.sh wos $bcp_dir pubcountry       WoSTestPubCountryStaging       &
      sleep 10
      $controller_dir/load_daemon.sh wos $bcp_dir pubsubject       WoSTestPubSubjectStaging       &
  
      wait # For them all to finish

      exit 0
      ;;
    "MARK_COMPLETE")
      $db_dir/wos/PrepareForImport.sh $bcp_dir/complete.
      exit 0
      ;;
    "affiliation" | "author" | "grant" | "source")
      bcp_needs_sorting=1
      ;;
    *)
      bcp_needs_sorting=0
      ;;
  esac
fi

buffer_file=$bcp_dir/${type}.bcp
buffer_count=0
buffer_limit=10000000    # Maybe vary this if sorting is or is not needed
                         # And maybe double each time limit is reached? Maybe not

finished=0

while [ $finished -le 0 ]
do
  ready_files=$(ls $bcp_dir/*.${type}.ready 2>/dev/null)

  if [ "z$ready_files" != "z" ]  # Something found
  then
    for ready_file in $ready_files
    do 
      rm $ready_file

      bcp_file=${ready_file//.ready/.bcp}

      if [[ $ready_file =~ '/complete.' ]]
      then
        finished=1
        buffer_count=$buffer_limit # Force dump
      else
        let "buffer_count += $(wc $bcp_file -l | cut -d' ' -f1)"

        if [[ $bcp_needs_sorting -eq 1 ]] 
        then
          sort -u $bcp_file -T $bcp_dir >> $buffer_file
          rm $bcp_file
        else
          if [ -f $buffer_file ]
          then
            cat $bcp_file >> $buffer_file
            rm $bcp_file
          else
            mv $bcp_file $buffer_file
          fi
        fi
      fi
    done

    if [[ $buffer_count -ge $buffer_limit && -f $buffer_file ]]  # On final round buffer file might not exist
    then
      # Need to dump it
      if [ $bcp_needs_sorting -eq 1 ]
      then
        sort -u $buffer_file -T $bcp_dir > $buffer_file.sorted && mv $buffer_file.sorted $buffer_file
      fi

      if [[ $update == "update" && $type == "publication" ]] # type check is paranoia. Or future proofing AMB 28.12.24
      then
        $db_dir/$supplier/CleanPublicationStaging.sh $buffer_file
      fi

      $db_dir/ImportTable.sh $table $buffer_file

      rm $buffer_file

      buffer_count=0
    fi
  fi
  
  sleep 10
done

# Now we're done, get stats on the table

psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "ANALYSE \"$table\";"

exit 0
