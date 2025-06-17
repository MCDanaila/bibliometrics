DROP TABLE IF EXISTS "WoSTestCitation";

CREATE TABLE "WoSTestCitation"
(
  referencing_id INTEGER,
  referenced_id  INTEGER
);

GRANT SELECT ON TABLE "WoSTestCitation" TO "biblio01";
