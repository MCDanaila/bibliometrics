DROP TABLE IF EXISTS "ScopusTestPublication" ;

CREATE TABLE "ScopusTestPublication"
(
  id                   BIGINT      ,
  sgrid                BIGINT  NULL,
  source_id            BIGINT  NULL,
  doi                  VARCHAR NULL,
  ce_ern               VARCHAR NULL,
  publication_type     VARCHAR NULL,
  publication_language VARCHAR NULL,
  title                VARCHAR NULL,
  english_title        VARCHAR NULL,
  alt_titles           VARCHAR NULL,
  publication_year     INT     NULL,
  publication_month    INT     NULL,
  publication_day      INT     NULL,
  volume               VARCHAR NULL,
  issue                VARCHAR NULL,
  page_first           VARCHAR NULL,
  page_last            VARCHAR NULL,
  copyright            VARCHAR NULL,
  abstract             VARCHAR NULL,
  is_open_access       VARCHAR NULL,
  oa_free_to_read      VARCHAR NULL,
  oa_status            VARCHAR NULL,
  xml_name             VARCHAR     ,
  zip_name             VARCHAR     ,
  version              CHAR(1)
) ;
