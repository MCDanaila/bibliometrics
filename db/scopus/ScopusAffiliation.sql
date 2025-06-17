DROP TABLE IF EXISTS "ScopusTestAffiliation";

CREATE TABLE "ScopusTestAffiliation"
(
  id           SERIAL      ,
  afid         BIGINT  NULL,
  dptid        BIGINT  NULL,
  organization VARCHAR NULL,
  country      VARCHAR NULL,
  address      VARCHAR NULL,
  city         VARCHAR NULL,
  hashval      VARCHAR     ,
  version      CHAR(1)
);

DROP TABLE IF EXISTS "ScopusTestAffiliationStaging";

CREATE TABLE "ScopusTestAffiliationStaging"
(
  afid         BIGINT  NULL,
  dptid        BIGINT  NULL,
  organization VARCHAR NULL,
  country      VARCHAR NULL,
  address      VARCHAR NULL,
  city         VARCHAR NULL,
  hashval      VARCHAR     ,
  version      CHAR(1)
);
