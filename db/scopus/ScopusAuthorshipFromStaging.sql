CREATE INDEX IF NOT EXISTS scopusTest_autship_staging_temp on "ScopusTestAuthorshipWithAffiliationId" (author_hash);

BEGIN;
INSERT INTO "ScopusTestAuthorship" (
  pub_id        ,
  author_id     ,
  int_author_id ,
  affiliation_id,
  seq           ,
  version       ) 
SELECT st.pub_id        ,
       st.scopus_aut_id ,
       aut.id           ,
       st.affiliation_id,
       st.seq           ,
       st.version
FROM   "ScopusTestAuthorshipWithAffiliationId" st ,
       "ScopusTestAuthor"                      aut
WHERE  aut.hashval = st.author_hash      -- Should check uniqueness before running
;
COMMIT;

DROP INDEX scopusTest_autship_staging_temp; -- Why? AMB 20.12.23
