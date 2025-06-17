db_dir=$(dirname $0)
db_script_dir=$db_dir/..

# The indexes can be created in parallel, but it would hammer the database

$db_script_dir/CreateIndexes.sh WoSAffiliation
$db_script_dir/CreateIndexes.sh WoSAuthor
$db_script_dir/CreateIndexes.sh WoSAuthorship
$db_script_dir/CreateIndexes.sh WoSPublication
$db_script_dir/CreateIndexes.sh WoSSource
$db_script_dir/CreateIndexes.sh WoSPubCountry
$db_script_dir/CreateIndexes.sh WoSPubOrg

