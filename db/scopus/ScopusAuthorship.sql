DROP TABLE IF EXISTS "ScopusTestAuthorship";

CREATE TABLE "ScopusTestAuthorship"
(
  pub_id         BIGINT ,
  author_id      BIGINT ,
  int_author_id  BIGINT ,
  affiliation_id BIGINT ,  
  seq            INTEGER,
  version        CHAR(1)
);

DROP TABLE IF EXISTS "ScopusTestAuthorshipStaging";

CREATE TABLE "ScopusTestAuthorshipStaging"
(
  pub_id           BIGINT      ,
  seq              INTEGER     ,
  scopus_aut_id    BIGINT      ,
  -- Author details
  degrees          VARCHAR NULL,
  given_name       VARCHAR NULL,
  surname          VARCHAR NULL,
  indexed_name     VARCHAR NULL,
  preferred_name   VARCHAR NULL,
  e_address        VARCHAR NULL,
  -- affiliation details
  afid             BIGINT  NULL,
  dptid            BIGINT  NULL,
  organization     VARCHAR NULL,
  country          VARCHAR NULL,
  address          VARCHAR NULL,
  city             VARCHAR NULL,
  -- and hash values
  author_hash      VARCHAR     ,
  affiliation_hash VARCHAR     ,
  version          CHAR(1) 
);

DROP TABLE IF EXISTS "ScopusTestAuthorshipWithAffiliationId";

CREATE TABLE "ScopusTestAuthorshipWithAffiliationId"
(
  pub_id           BIGINT      ,
  seq              INTEGER     ,
  scopus_aut_id    BIGINT      ,
  affiliation_id   BIGINT      ,  
  -- Author details
  degrees          VARCHAR NULL,
  given_name       VARCHAR NULL,
  surname          VARCHAR NULL,
  indexed_name     VARCHAR NULL,
  preferred_name   VARCHAR NULL,
  e_address        VARCHAR NULL,
  author_hash      VARCHAR     ,
  version          CHAR(1) 
);
