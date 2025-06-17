\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true
SELECT CONCAT( 'WoSPubCountryFromStaging staging starting at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

INSERT INTO "WoSTestPubCountry"
(
  pub_id ,
  country
)
SELECT p.id, st.country
FROM   "WoSTestPubCountryStaging" st,
       "WoSTestPublication"       p
WHERE  st.pub_wos_hash = p.wos_hash ;

ANALYZE  "WoSTestPubCountry" ;

SELECT CONCAT( 'WoSPubCountryFromStaging staging finishing at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
