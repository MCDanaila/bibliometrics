\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true
SELECT CONCAT( 'WoSPubOrgFromStaging staging starting at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

INSERT INTO "WoSTestPubOrg"
(
  pub_id      ,
  unified_name
)
SELECT p.id, st.unified_name
FROM   "WoSTestPubOrgStaging" st,
       "WoSTestPublication"   p
WHERE  st.pub_wos_hash = p.wos_hash ;

ANALYZE  "WoSTestPubOrg" ;

SELECT CONCAT( 'WoSPubOrgFromStaging staging finishing at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
