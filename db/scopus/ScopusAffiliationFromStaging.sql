DROP INDEX IF EXISTS scopusTest_aff_1;

INSERT INTO "ScopusTestAffiliation"
( afid, dptid, organization, country, address, city, hashval, version)
SELECT 
DISTINCT afid, dptid, organization, country, address, city, hashval, version
FROM "ScopusTestAffiliationStaging";

CREATE INDEX scopusTest_aff_1 ON "ScopusTestAffiliation" (hashval)

-- TRUNCATE "ScopusTestAffiliationStaging";
