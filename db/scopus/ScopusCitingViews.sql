DROP VIEW IF EXISTS "ScopusTestCitedBy";

CREATE VIEW "ScopusTestCitedBy" AS
(SELECT 
cited_id as pub_id,
count(*) as cited_by_count
FROM "ScopusTestCitation"
group by cited_id);

DROP VIEW IF EXISTS "ScopusTestCiting";

CREATE VIEW "ScopusTestCiting" AS
(SELECT 
citing_id as pub_id,
count(*) as citing_count
FROM "ScopusTestCitation"
group by citing_id);
