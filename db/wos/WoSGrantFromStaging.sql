\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true
SELECT CONCAT( 'WoSGrantFromStaging staging starting at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

INSERT INTO "WoSTestGrant"
( grant_agencies, grant_ids, hashval)
SELECT DISTINCT ON (hashval) 
grant_agencies, grant_ids, hashval
FROM "WoSTestGrantStaging";

ANALYZE "WoSTestGrant" ;

SELECT CONCAT( 'WoSGrantFromStaging staging finishing at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

-- While developing retain TRUNCATE "WoSTestGrantStaging";

