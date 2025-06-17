ROOT_NAME=$1
SOURCE_NAME=$2
TEST_NAME=${ROOT_NAME//$SOURCE_NAME/${SOURCE_NAME}Test}

echo "Root   name    is [$ROOT_NAME]"
echo "Source name    is [$SOURCE_NAME]"
echo "Test   name    is [$TEST_NAME]"
echo "Command drop   is [DROP TABLE \"$ROOT_NAME\"]"
echo "Command rename is [ALTER TABLE \"$TEST_NAME\" RENAME TO \"$ROOT_NAME\"]"

echo "DROP TABLE \"$ROOT_NAME\"" |\
psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER

echo "ALTER TABLE \"$TEST_NAME\" RENAME TO \"$ROOT_NAME\"" |\
psql -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER
