#!/bin/bash

work_dir=$1

echo "Cleaning [$work_dir] as working area"

if [[ ! -d $work_dir ]]
then
  echo "$work_dir is not a directory"
  exit -1
fi

for type in "xml" "bcp" "done" "updates"
do
  dir_to_process=$work_dir/${type}
  if [ -d $dir_to_process ]
  then
    # to_be_deleted=${dir_to_process}_delete_me
    # mv $dir_to_process $to_be_deleted

    rm -rf $dir_to_process
  fi
  mkdir $dir_to_process
done

