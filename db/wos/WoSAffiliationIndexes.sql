\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true

SELECT CONCAT( 'WoSTestAffiliation_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE UNIQUE INDEX "WoSTestAffiliation_id" ON "WoSTestAffiliation" ( id) ;

SELECT CONCAT( 'WoSTestAffiliation_unified_names index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestAffiliation_unified_names" ON "WoSTestAffiliation" ( org_unified_names, id) ;

SELECT CONCAT( 'WoSTestAffiliation_country index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestAffiliation_country" ON "WoSTestAffiliation" ( country) ;

SELECT CONCAT( 'WoSTestAffiliation post index analyze started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
ANALYZE "WoSTestAffiliation" ;

SELECT CONCAT( 'WoSTestAffiliation index finished at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
