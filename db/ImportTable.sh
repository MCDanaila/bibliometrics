table_name=$1
file_name=$2

# Need to remove all indexes

indexes_to_drop=$(psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c \
"SELECT indexname FROM pg_indexes WHERE tablename = '$table_name'")

for index_to_drop in $indexes_to_drop
do
  psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "DROP INDEX IF EXISTS \"$index_to_drop\";"
done

psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -c "\COPY \"$table_name\" FROM '$file_name' with DELIMITER '	'  NULL as '';"

