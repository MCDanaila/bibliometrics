bcp_file=$1
bcp_file_deletes=${bcp_file}_deletion_list

echo "Bcp file is [$bcp_file] and deletions_file is [$bcp_file_deletes]"

awk -F'\t' '{print $1}' $bcp_file > $bcp_file_deletes

sql_file="/tmp/CleanPublicationStaging_$$.sql"

delete_ids_table=temp_delete_details_$$
staging_idx=temp_staging_index_$$

cat  << EOF > $sql_file
\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true

SELECT CONCAT( 'CleanPublicationStaging started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

CREATE TABLE $delete_ids_table( wos_hash BIGINT);
\COPY $delete_ids_table FROM '$bcp_file_deletes'; 
CREATE INDEX ${delete_ids_table}_idx ON $delete_ids_table ( wos_hash);

SELECT CONCAT( 'CleanPublicationStaging WoSTestPublicationStaging cleaning started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

CREATE INDEX $staging_idx ON "WoSTestPublicationStaging" (wos_hash) ;
ANALYZE "WoSTestPublicationStaging" ;
DELETE FROM "WoSTestPublicationStaging" t USING $delete_ids_table dit WHERE dit.wos_hash = t.wos_hash ;
DROP INDEX $staging_idx;

SELECT CONCAT( 'CleanPublicationStaging WoSTestAuthorKeywordStaging cleaning started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

CREATE INDEX $staging_idx ON "WoSTestAuthorKeywordStaging" (pub_wos_hash) ;
DELETE FROM "WoSTestAuthorKeywordStaging" t USING $delete_ids_table dit WHERE dit.wos_hash = t.pub_wos_hash ;
DROP INDEX $staging_idx;

SELECT CONCAT( 'CleanPublicationStaging WoSTestAuthorshipStaging cleaning started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

CREATE INDEX $staging_idx ON "WoSTestAuthorshipStaging" (pub_wos_hash) ;
DELETE FROM "WoSTestAuthorshipStaging" t USING $delete_ids_table dit WHERE dit.wos_hash = t.pub_wos_hash ;
DROP INDEX $staging_idx;

SELECT CONCAT( 'CleanPublicationStaging WoSTestCitationStaging referencing cleaning started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

CREATE INDEX $staging_idx ON "WoSTestCitationStaging" (referencing_pub_hash) ;
DELETE FROM "WoSTestCitationStaging" t USING $delete_ids_table dit WHERE dit.wos_hash = t.referencing_pub_hash ;
DROP INDEX $staging_idx;

SELECT CONCAT( 'CleanPublicationStaging WoSTestCitationStaging referenced cleaning started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

CREATE INDEX $staging_idx ON "WoSTestCitationStaging" (referenced_pub_hash) ;
DELETE FROM "WoSTestCitationStaging" t USING $delete_ids_table dit WHERE dit.wos_hash = t.referenced_pub_hash ;
DROP INDEX $staging_idx;

SELECT CONCAT( 'CleanPublicationStaging WoSTestPubCountryStaging cleaning started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

CREATE INDEX $staging_idx ON "WoSTestPubCountryStaging" (pub_wos_hash) ;
DELETE FROM "WoSTestPubCountryStaging" t USING $delete_ids_table dit WHERE dit.wos_hash = t.pub_wos_hash ;
DROP INDEX $staging_idx;

SELECT CONCAT( 'CleanPublicationStaging WoSTestPubOrgStaging cleaning started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

CREATE INDEX $staging_idx ON "WoSTestPubOrgStaging" (pub_wos_hash) ;
DELETE FROM "WoSTestPubOrgStaging" t USING $delete_ids_table dit WHERE dit.wos_hash = t.pub_wos_hash ;
DROP INDEX $staging_idx;

SELECT CONCAT( 'CleanPublicationStaging WoSTestPubSubjectStaging cleaning started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

CREATE INDEX $staging_idx ON "WoSTestPubSubjectStaging" (pub_wos_hash) ;
DELETE FROM "WoSTestPubSubjectStaging" t USING $delete_ids_table dit WHERE dit.wos_hash = t.pub_wos_hash ;
DROP INDEX $staging_idx;

SELECT CONCAT( 'CleanPublicationStaging WoSTestPublicationGrantStaging cleaning started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

CREATE INDEX $staging_idx ON "WoSTestPublicationGrantStaging" (pub_wos_hash) ;
DELETE FROM "WoSTestPublicationGrantStaging" t USING $delete_ids_table dit WHERE dit.wos_hash = t.pub_wos_hash ;
DROP INDEX $staging_idx;
SELECT CONCAT( 'CleanPublicationStaging WoSTestPublicationStaging ended at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

-- After debug DROP TABLE $delete_ids_table
EOF

psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f $sql_file

rm $sql_file
rm $bcp_file_deletes
