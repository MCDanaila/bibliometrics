\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true
SELECT CONCAT( 'WoSAuthorshipGetAffiliation staging starting at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

DROP INDEX IF EXISTS wosTest_authorship_staging_affiliation_hash ;
DROP INDEX IF EXISTS wosTest_affiliation_hashval                 ;

CREATE INDEX wosTest_authorship_staging_affiliation_hash on "WoSTestAuthorshipStaging" (affiliation_hash);
CREATE INDEX wosTest_affiliation_hashval                 on "WoSTestAffiliation"       (hashval, id     );

SELECT CONCAT( 'WoSAuthorshipGetAffiliation staging post index at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

INSERT INTO "WoSTestAuthorshipAffIdStaging"
(
  pub_id        ,
  seq           ,
  affiliation_id,
  role          ,
  author_hash
)
SELECT p.id            ,
       st.seq          ,
       aff.id          ,
       role            ,
       author_hash
FROM   "WoSTestAuthorshipStaging" st ,
       "WoSTestPublication"       p  ,
       "WoSTestAffiliation"       aff
WHERE  aff.hashval = st.affiliation_hash 
AND    p.wos_hash  = st.pub_wos_hash    ;

ANALYZE "WoSTestAuthorshipAffIdStaging" ;

SELECT CONCAT( 'WoSAuthorshipGetAffiliation staging finishing at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
