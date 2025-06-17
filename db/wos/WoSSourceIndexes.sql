\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true

SELECT CONCAT( 'WoSTestSource_id_name index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE UNIQUE INDEX "WoSTestSource_id" ON "WoSTestSource" (id, name) ;

SELECT CONCAT( 'WoSTestSource post index analyze started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
ANALYZE "WoSTestSource" ;

SELECT CONCAT( 'WoSTestSource index finished at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
