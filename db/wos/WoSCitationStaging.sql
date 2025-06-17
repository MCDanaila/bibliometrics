DROP TABLE IF EXISTS "WoSTestCitationStaging";

CREATE TABLE "WoSTestCitationStaging"
(
  referencing_pub_hash BIGINT,
  referenced_pub_hash  BIGINT
);
