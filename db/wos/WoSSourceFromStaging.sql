\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true
SELECT CONCAT( 'WoSSourceFromStaging staging starting at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

INSERT INTO "WoSTestSource"
( name, issn, abbrev, publisher, source_abbrev, abbrev_iso, abbrev_11, abbrev_29, hashval)
SELECT
DISTINCT ON (hashval)
name, issn, abbrev, publisher, source_abbrev, abbrev_iso, abbrev_11, abbrev_29, hashval
FROM "WoSTestSourceStaging";

ANALYZE "WoSTestSource" ;

SELECT CONCAT( 'WoSSourceFromStaging staging finishing at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

-- While developing retain TRUNCATE "WoSTestSourceStaging";

