sql_file="/tmp/CleanPublicationStaging_$$.sql"

delete_ids_table=temp_delete_details_$$
staging_idx=temp_staging_index_$$

echo -n "Stage 3 ($sql_file) : " ; date 
cat  << EOF > $sql_file
\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true

NOTE THAT THIS HAS NOT BEEN TESTED - AMB 31.12.2024

SELECT CONCAT( 'CleanPublicationStaging started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

CREATE TABLE $delete_ids_table AS SELECT wos_hash FROM "WoSTestPublicationStaging"
WHERE wos_hash NOT IN (SELECT wos_hash FROM "WoSTestPublication") ;
CREATE INDEX ${delete_ids_table}_idx ON $delete_ids_table ( wos_hash);

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
DELETE FROM "WoSTestPubOrgStaging" t USING $delete_ids_table dit WHERE dit.wos_hash = t.pub_wos_hash ;
DROP INDEX $staging_idx;

SELECT CONCAT( 'CleanPublicationStaging WoSTestPublicationGrantStaging cleaning started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

CREATE INDEX $staging_idx ON "WoSTestPublicationGrantStaging" (pub_wos_hash) ;
DELETE FROM "WoSTestPublicationGrantStaging" t USING $delete_ids_table dit WHERE dit.wos_hash = t.pub_wos_hash ;
DROP INDEX $staging_idx;

SELECT CONCAT( 'CleanPublicationStaging finished at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

DROP TABLE $delete_ids_table
EOF
echo -n "Stage 4 : " ; date 
psql -t -d $POSTGRES_DB -h $POSTGRES_SERVER -U $POSTGRES_USER -f $sql_file
echo -n "Stage 5 : " ; date 

rm $sql_file
