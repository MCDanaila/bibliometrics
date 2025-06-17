\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true
SELECT CONCAT( 'WoSPublicationFromStaging staging starting at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

DROP INDEX IF EXISTS wostest_publication_staging_src_hash ;
DROP INDEX IF EXISTS wostest_publication_staging_wos_hash ;
DROP INDEX IF EXISTS wostest_citation_staging_referenced  ;
DROP INDEX IF EXISTS wostest_source_hashval               ;
DROP INDEX IF EXISTS wostest_author_hashval               ;

CREATE INDEX wostest_publication_staging_src_hash ON "WoSTestPublicationStaging" ( src_hash           ) ;
CREATE INDEX wostest_publication_staging_wos_hash ON "WoSTestPublicationStaging" ( src_hash           ) ;
CREATE INDEX wostest_source_hashval               ON "WoSTestSource"             ( hashval            ) ;
CREATE INDEX wostest_citation_staging_referenced  ON "WoSTestCitationStaging"    ( referenced_pub_hash) ;

ANALYZE "WoSTestPublicationStaging" ;
ANALYZE "WoSTestSource"             ;

-- Where should this index be created? Probably on AuthorFromStaging
CREATE INDEX wostest_author_hashval ON "WoSTestAuthor" (hashval) ;

ANALYZE "WoSTestAuthor" ;

-- Get citation information

SELECT CONCAT( 'WoSPublicationFromStaging staging pre citation group at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

DROP TABLE IF EXISTS "WoSGroupingTemp" ;   -- Paranoia

CREATE TABLE "WoSGroupingTemp" AS SELECT   referenced_pub_hash, count(*) AS cnt
                                  FROM     "WoSTestCitationStaging" cg
                                  WHERE    referenced_pub_hash IN (SELECT wos_hash FROM "WoSTestPublicationStaging")
                                  GROUP BY referenced_pub_hash ;

CREATE INDEX "WoSGroupingTemp_ed_cnt" ON "WoSGroupingTemp" (referenced_pub_hash, cnt) ;

ANALYZE "WoSGroupingTemp" ;

SELECT CONCAT( 'WoSPublicationFromStaging staging post citation group at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

SELECT CONCAT( 'WoSPublicationFromStaging staging post indices at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

INSERT INTO "WoSTestPublication"
(
  wos_id              ,
  doi                 ,
  pmid                ,
  wos_publication_type,
  publication_language,
  title               ,
  page_first          ,
  page_last           ,
  publication_date    ,
  publication_year    ,
  publication_month   ,
  volume              ,
  copyright           ,
  wuid                ,
  headings            ,
  subheadings         ,
  subjects            ,
  abstract            ,
  source_id           ,
  fund_text           ,
  grant_id            ,
  oa_status           ,
  author_keywords     ,
  author_ids          ,
  countries           ,
  org_unified_names   ,
  is_retracted        ,
  publication_type    ,
  reference_count     ,
  citation_count      ,
  source_xml_file     ,
  wos_hash
)
WITH author_map AS 
( 
  SELECT st.wos_hash, ARRAY_AGG( a.id) as author_ids
  FROM   "WoSTestPublicationStaging" st
  JOIN   "WoSTestSource" src ON st.src_hash = src.hashval
  JOIN   UNNEST( st.author_hashes) AS amap( author_hash) ON TRUE
  JOIN   "WoSTestAuthor" a ON amap.author_hash = a.hashval
  GROUP BY st.wos_hash
)
SELECT st.wos_id              ,
       st.doi                 ,
       st.pmid                ,
       st.wos_publication_type,
       st.publication_language,
       st.title               ,
       st.page_first          ,
       st.page_last           ,
       st.publication_date    ,
       st.publication_year    ,
       st.publication_month   ,
       st.volume              ,
       st.copyright           ,
       st.wuid                ,
       st.headings            ,
       st.subheadings         ,
       st.subjects            ,
       st.abstract            ,
       src.id                 ,
       st.fund_text           ,
       st.grant_id            ,
       st.oa_status           ,
       st.author_keywords     ,
       author_ids             ,
       st.countries           ,
       st.org_unified_names   ,
       st.is_retracted        ,
       st.publication_type    ,
       st.reference_count     ,
       COALESCE( cg.cnt, 0)   ,
       st.source_xml_file     ,
       st.wos_hash
FROM            "WoSTestPublicationStaging" st
JOIN            author_map                  am  ON st.wos_hash = am.wos_hash 
JOIN            "WoSTestSource"             src ON st.src_hash = src.hashval
LEFT OUTER JOIN "WoSGroupingTemp"           cg  ON st.wos_hash = cg.referenced_pub_hash ;

SELECT CONCAT( 'WoSPublicationFromStaging staging post insert at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

DROP          INDEX IF EXISTS "WoSTestPublication_wos_hash_id"                                        ;
CREATE UNIQUE INDEX           "WoSTestPublication_wos_hash_id" ON "WoSTestPublication" (wos_hash, id) ;

ANALYZE "WoSTestPublication";

SELECT CONCAT( 'WoSPublicationFromStaging staging finishing at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

DROP TABLE "WoSGroupingTemp" ;

-- TRUNCATE "WoSTestPublicationStaging";  -- Maybe drop table in prod? AMB 23/7/23
