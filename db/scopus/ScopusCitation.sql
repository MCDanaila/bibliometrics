DROP TABLE IF EXISTS "ScopusTestCitation";

CREATE TABLE "ScopusTestCitation"
(
  citing_id BIGINT,
  cited_id  BIGINT,
  version   CHAR(1)
);
