DROP TABLE IF EXISTS "WoSTestAffiliationStaging";

CREATE TABLE "WoSTestAffiliationStaging"
(
  organization	    VARCHAR       ,
  org_unified_names VARCHAR[]     ,
  sub_organizations	VARCHAR[] NULL,
  address	          VARCHAR   NULL,
  country	          VARCHAR   NULL,
  state	            VARCHAR   NULL,
  city	            VARCHAR   NULL,
  street	          VARCHAR   NULL,
  postal_code	      VARCHAR   NULL,
  ror_id	          VARCHAR   NULL,
  org_id	          VARCHAR   NULL,
  hashval           BIGINT
);
