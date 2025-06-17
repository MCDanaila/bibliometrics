\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true

SELECT CONCAT( 'WoSTestPubCountry_country_pub_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE UNIQUE INDEX "WoSTestPubCountry_country_pub_id" ON "WoSTestPubCountry" (country, pub_id) ;

SELECT CONCAT( 'WoSTestPubCountry post index analyze started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
ANALYZE "WoSTestPubCountry" ;

SELECT CONCAT( 'WoSTestPubCountry index finished at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
