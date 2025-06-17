DROP TABLE IF EXISTS "WoSTestGrantStaging";

CREATE TABLE "WoSTestGrantStaging"
(
  grant_agencies VARCHAR[],
  grant_ids      VARCHAR[],
  hashval        BIGINT
) ;
