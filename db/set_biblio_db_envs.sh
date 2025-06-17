#!/bin/bash

# Does .pgpass exist

if [[ $PGPASSFILE == "" ]]
then
  pwd_file=/home/bibliometric/.pgpass
else
  pwd_file=$PGPASSFILE
fi

echo $pwd_file

if [[ ! -f $pwd_file ]]
then
  echo "No password file $pwd_file found"
  exit -1
fi

db_details=$(head -1 $pwd_file)
export POSTGRES_SERVER=$(echo $db_details | awk -F: '{print $1}')
export POSTGRES_DB=$(echo $db_details | awk -F: '{print $3}')
export POSTGRES_USER=$(echo $db_details | awk -F: '{print $4}')
export POSTGRES_PASSWD=$(echo $db_details | awk -F: '{print $5}')

echo "POSTGRES_SERVER is $POSTGRES_SERVER"
echo "POSTGRES_DB     is $POSTGRES_DB"
echo "POSTGRES_USER   is $POSTGRES_USER"
echo "POSTGRES_PASSWD is $POSTGRES_PASSWD"
