\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true
SELECT CONCAT( 'WoSAuthorshipFromStaging staging starting at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

DROP INDEX IF EXISTS wostest_authorshipwithaffiliationid_author_hash; 
DROP INDEX IF EXISTS wostest_author_hashval                         ; 

CREATE INDEX wostest_authorshipwithaffiliationid_author_hash ON "WoSTestAuthorshipAffIdStaging" (author_hash);
CREATE INDEX wostest_author_hashval                          ON "WoSTestAuthor"                 (hashval    );

ANALYZE "WoSTestAuthorshipAffIdStaging";
ANALYZE "WoSTestAuthor"                ;

SELECT CONCAT( 'WoSAuthorshipFromStaging staging post index at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

INSERT INTO "WoSTestAuthorship" (
  pub_id        ,
  int_author_id ,
  affiliation_id,
  role          ,
  seq
  ) 
SELECT st.pub_id        ,
       aut.id           ,
       st.affiliation_id,
       st.role          ,
       st.seq
FROM   "WoSTestAuthorshipAffIdStaging" st ,
       "WoSTestAuthor"                 aut
WHERE  aut.hashval = st.author_hash;

ANALYZE "WoSTestAuthorship" ;

SELECT CONCAT( 'WoSAuthorshipFromStaging staging finishing at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

-- TRUNCATE "WoSTestAuthorshipStaging";  -- Maybe drop table in prod? AMB 23/7/23
