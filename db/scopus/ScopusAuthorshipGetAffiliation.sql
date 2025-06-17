CREATE INDEX IF NOT EXISTS scopusTest_autship_staging_temp on "ScopusTestAuthorshipStaging" (affiliation_hash);

INSERT INTO "ScopusTestAuthorshipWithAffiliationId"
(
  pub_id        ,
  seq           ,
  scopus_aut_id ,
  affiliation_id,
  degrees       ,
  given_name    ,
  surname       ,
  indexed_name  ,
  preferred_name,
  e_address     ,
  author_hash   ,
  version
)
SELECT DISTINCT 
       st.pub_id        ,
       st.seq           ,
       st.scopus_aut_id ,
       aff.id           ,
       st.degrees       ,
       st.given_name    ,
       st.surname       ,
       st.indexed_name  ,
       st.preferred_name,
       st.e_address     ,
       st.author_hash   ,
       st.version
FROM   "ScopusTestAuthorshipStaging" st ,
       "ScopusTestAffiliation"       aff
WHERE  aff.hashval = st.affiliation_hash ;

DROP INDEX scopusTest_autship_staging_temp;
