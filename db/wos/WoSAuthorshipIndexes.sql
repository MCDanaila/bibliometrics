\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true

SELECT CONCAT( 'WoSTestAuthorship_pub_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestAuthorship_pub_id" ON "WoSTestAuthorship" (pub_id) ;

SELECT CONCAT( 'WoSTestAuthorship_author_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestAuthorship_author_id" ON "WoSTestAuthorship" ( int_author_id) ;

SELECT CONCAT( 'WoSTestAuthorship_affiliation_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestAuthorship_affiliation_id" ON "WoSTestAuthorship" (affiliation_id, pub_id) ;

SELECT CONCAT( 'WoSTestAuthorship post index analyze started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
ANALYZE "WoSTestAuthorship" ;

SELECT CONCAT( 'WoSTestAuthorship index finished at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
