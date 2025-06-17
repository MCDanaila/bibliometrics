DROP TABLE IF EXISTS "WoSTestPublication" ;

CREATE TABLE "WoSTestPublication"
(
  id                   SERIAL        ,
  wos_id               VARCHAR       ,
  doi                  VARCHAR   NULL,
  pmid                 VARCHAR   NULL,
  wos_publication_type VARCHAR[] NULL,
  publication_language VARCHAR[] NULL,
  title                VARCHAR   NULL,
  page_first           VARCHAR   NULL,
  page_last            VARCHAR   NULL,
  publication_date     VARCHAR   NULL,
  publication_year     SMALLINT  NULL,
  publication_month    VARCHAR   NULL,
  volume               VARCHAR   NULL,
  copyright            VARCHAR   NULL,
  wuid                 VARCHAR   NULL,
  headings             VARCHAR[] NULL,
  subheadings          VARCHAR[] NULL,
  subjects             VARCHAR[] NULL,
  abstract             VARCHAR   NULL,
  source_id            INT       NULL,
  fund_text            VARCHAR   NULL,
  grant_id             INT       NULL,
  oa_status            VARCHAR   NULL,
  author_keywords      VARCHAR[] NULL,
  author_ids           INT[]     NULL,
  reference_count      INT       NULL,
  citation_count       INT       NULL,
  countries            VARCHAR[] NULL,
  org_unified_names    VARCHAR[] NULL,
  is_retracted         SMALLINT  NULL,
  publication_type     VARCHAR   NULL,
  wos_hash             BIGINT        ,
  source_xml_file      VARCHAR   NULL
) ;

GRANT SELECT ON TABLE "WoSTestPublication" TO "biblio01";
