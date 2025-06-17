DROP TABLE IF EXISTS "WoSTestPubOrg";

CREATE TABLE "WoSTestPubOrg"
(
  pub_id       INTEGER,
  unified_name VARCHAR
);

GRANT SELECT ON TABLE "WoSTestPubOrg" TO "biblio01";
