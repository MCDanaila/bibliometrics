DROP INDEX IF EXISTS scopusTest_aut_1;
DROP INDEX IF EXISTS scopusTest_aut_2;

INSERT INTO "ScopusTestAuthor"
( scopus_id, degrees, given_name, surname, indexed_name, preferred_name, e_address, hashval, version)
SELECT 
DISTINCT scopus_id, degrees, given_name, surname, indexed_name, preferred_name, e_address, hashval, version
FROM "ScopusTestAuthorStaging";
ANALYZE "ScopusTestAuthor";

CREATE INDEX scopusTest_aut_1 ON "ScopusTestAuthor" (scopus_id, id);
CREATE INDEX scopusTest_aut_2 ON "ScopusTestAuthor" (hashval);

-- TRUNCATE "ScopusTestAuthorStaging";
