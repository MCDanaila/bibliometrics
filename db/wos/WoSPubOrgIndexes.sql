\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true

SELECT CONCAT( 'WoSTestPubOrg_unified_name_pub_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE UNIQUE INDEX "WoSTestPubOrg_unified_name_pub_id" ON "WoSTestPubOrg" (unified_name, pub_id) ;

SELECT CONCAT( 'WoSTestPubOrg_pub_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestPubOrg_pub_id" ON "WoSTestPubOrg" (pub_id) ;

SELECT CONCAT( 'WoSTestPubOrg post index analyze started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
ANALYZE "WoSTestPubOrg" ;

SELECT CONCAT( 'WoSTestPubOrg index finished at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
