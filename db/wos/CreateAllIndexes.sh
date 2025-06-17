db_dir=$(dirname $0)
db_script_dir=$db_dir/..

# The indexes can be created in parallel, but it would hammer the database

$db_script_dir/CreateIndexes.sh WoSTestAffiliation
$db_script_dir/CreateIndexes.sh WoSTestAuthor
$db_script_dir/CreateIndexes.sh WoSTestAuthorKeyword
$db_script_dir/CreateIndexes.sh WoSTestAuthorship
$db_script_dir/CreateIndexes.sh WoSTestPublication
$db_script_dir/CreateIndexes.sh WoSTestCitation
$db_script_dir/CreateIndexes.sh WoSTestSource
$db_script_dir/CreateIndexes.sh WoSTestPubCountry
$db_script_dir/CreateIndexes.sh WoSTestPubOrg

