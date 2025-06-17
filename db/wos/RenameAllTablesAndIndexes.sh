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

test_tables=$(psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c \
"SELECT tablename FROM pg_tables WHERE tablename LIKE 'WoSTest%' AND tablename NOT LIKE 'WoSTest%Staging%'")

for test_table in $test_tables
do
  table_to_drop=${test_table/WoSTest/WoS}
  echo "Running: DROP TABLE IF EXISTS \"$table_to_drop\";"
  psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "DROP TABLE IF EXISTS \"$table_to_drop\";"
done

for test_table in $test_tables
do
  new_table=${test_table/WoSTest/WoS}
  echo "Running: ALTER TABLE \"$test_table\" RENAME TO \"$new_table\";"
  psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "ALTER TABLE \"$test_table\" RENAME TO \"$new_table\";"
done

test_indexes=$(psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c \
"SELECT indexname FROM pg_indexes WHERE indexname LIKE 'WoSTest%'")

for test_index in $test_indexes
do
  new_name=${test_index/Test/test}
  new_name=${new_name/test/}
  echo "Running: ALTER INDEX \"$test_index\" RENAME TO \"$new_name\";"
  psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "ALTER INDEX \"$test_index\" RENAME TO \"$new_name\";"
done

# psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f $(dirname $0)/*/${table_name/Test}Indexes.sql

staging_tables=$(psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c \
"SELECT tablename FROM pg_tables WHERE tablename LIKE 'WoSTest%Staging%'")

for staging_table in $staging_tables
do
  echo "Running: DROP TABLE \"$staging_table\";"  
  psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "DROP TABLE \"$staging_table\";"
done

