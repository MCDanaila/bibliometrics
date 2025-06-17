DROP TABLE IF EXISTS "WoSTestAuthorship";

CREATE TABLE "WoSTestAuthorship"
(
  pub_id         INTEGER,
  role           VARCHAR,
  int_author_id  BIGINT ,
  affiliation_id BIGINT ,  
  seq            INTEGER
);

GRANT SELECT ON TABLE "WoSTestAuthorship" TO "biblio01";

DROP TABLE IF EXISTS "WoSTestAuthorshipStaging";

CREATE TABLE "WoSTestAuthorshipStaging"
(
  pub_wos_hash      BIGINT   ,
  seq               INTEGER     ,
  role              VARCHAR     ,
  author_hash       BIGINT   ,
  -- affiliation details
  organization      VARCHAR     ,
  org_unified_names VARCHAR NULL,
  sub_organizations VARCHAR NULL,
  address           VARCHAR NULL,
  country           VARCHAR NULL,
  state             VARCHAR NULL,
  city              VARCHAR NULL,
  street            VARCHAR NULL,
  postal_code       VARCHAR NULL,
  ror_id	          VARCHAR NULL,
  org_id	          VARCHAR NULL,
  affiliation_hash  BIGINT
);

DROP TABLE IF EXISTS "WoSTestAuthorshipAffIdStaging";

CREATE TABLE "WoSTestAuthorshipAffIdStaging"
(
  pub_id            INTEGER  ,
  seq               INTEGER  ,
  role              VARCHAR  ,
  affiliation_id    BIGINT   ,
  -- Author details
  author_hash       BIGINT
);

