INSERT INTO "ScopusTestSource"
( id, name, abbrev, issn, codencode, publisher, version)
SELECT 
DISTINCT id, name, abbrev, issn, codencode, publisher, version
FROM "ScopusTestSourceStaging";
ANALYZE "ScopusTestSource";

-- TRUNCATE "ScopusTestSourceStaging";
