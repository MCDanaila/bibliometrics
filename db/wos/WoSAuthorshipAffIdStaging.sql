/*
This is a badly named table - it's a sort of staging but everything else is populated from
python, not sql. AMB 30.12.24
*/

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

