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
  ror_id	          VARCHAR   NULL,
  org_id	          VARCHAR   NULL,
  affiliation_hash  BIGINT
);
