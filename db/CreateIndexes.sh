table_name=$1
provider=$2

# Need to remove all indexes

indexes_to_drop=$(psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c \
"SELECT indexname FROM pg_indexes WHERE tablename = '$table_name'")

for index_to_drop in $indexes_to_drop
do
  psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "DROP INDEX IF EXISTS \"$index_to_drop\";"
done

db_dir=$(dirname $0)

psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f $(dirname $0)/${provider}/${table_name/Test}Indexes.sql

