DROP TABLE IF EXISTS "WoSTestPubCountry";

CREATE TABLE "WoSTestPubCountry"
(
  pub_id  INTEGER,
  country VARCHAR
);

GRANT SELECT ON TABLE "WoSTestPubCountry" TO "biblio01";
