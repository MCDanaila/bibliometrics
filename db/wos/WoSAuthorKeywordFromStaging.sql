\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true
SELECT CONCAT( 'WoSAuthorKeywordFromStaging staging starting at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

INSERT INTO "WoSTestAuthorKeyword"
(
  pub_id ,
  keyword
)
SELECT p.id, st.keyword
FROM   "WoSTestAuthorKeywordStaging" st,
       "WoSTestPublication"          p
WHERE  st.pub_wos_hash = p.wos_hash ;

ANALYZE  "WoSTestAuthorKeyword" ;

SELECT CONCAT( 'WoSAuthorKeywordFromStaging staging finishing at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
