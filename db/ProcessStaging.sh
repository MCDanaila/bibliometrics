table_name=$1
sql_dir=`dirname $0`
sql_file=$sql_dir/$2
provider=$(echo $2 | sed 's/\/.*//')

# Recreate table. At the moment need to remove Test from the table name - this needs to be addressed
# With the new method, WoSTest tables aren't really needed. If paranoid, the process.sh should be 
# changed so that Staging processing be run manualy from another script

psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f $sql_dir/$provider/${table_name/Test/}.sql

psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f $sql_file
