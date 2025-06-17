DROP TABLE IF EXISTS "WoSTestPublicationStaging" ;

CREATE TABLE "WoSTestPublicationStaging"
(
  wos_hash             BIGINT          ,   -- Best to keep this in the first column for updating maintenance
  -- Pure publication
  wos_id               VARCHAR         ,
  doi                  VARCHAR     NULL,
  pmid                 VARCHAR     NULL,
  wos_publication_type VARCHAR[]   NULL,
  publication_language VARCHAR[]   NULL,
  title                VARCHAR     NULL,
  page_first           VARCHAR     NULL,
  page_last            VARCHAR     NULL,
  publication_date     VARCHAR     NULL,
  publication_year     SMALLINT    NULL,
  publication_month    VARCHAR     NULL,
  volume               VARCHAR     NULL,
  copyright            VARCHAR     NULL,
  wuid                 VARCHAR[]   NULL,
  headings             VARCHAR[]   NULL,
  subheadings          VARCHAR[]   NULL,
  subjects             VARCHAR[]   NULL,
  abstract             VARCHAR     NULL,
  fund_text            VARCHAR     NULL,
  grant_id             INT         NULL,
  oa_status            VARCHAR     NULL,
  author_keywords      VARCHAR[]   NULL,
  author_hashes        BIGINT[]    NULL,
  reference_count      INT         NULL,
  countries            VARCHAR[]   NULL,
  org_unified_names    VARCHAR[]   NULL,
  is_retracted         SMALLINT    NULL,
  publication_type     VARCHAR     NULL,
  source_xml_file      VARCHAR     NULL,
  -- Source linkage
  src_hash             BIGINT
) ;
