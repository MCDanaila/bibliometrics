\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true
SELECT CONCAT( 'WoSAffiliationFromStaging staging starting at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

INSERT INTO "WoSTestAffiliation"
( organization, org_unified_names, sub_organizations, address, country, state, city, street, postal_code, ror_id, org_id, hashval)
SELECT 
DISTINCT ON ( hashval)
organization, org_unified_names, sub_organizations, address, country, state, city, street, postal_code, ror_id, org_id, hashval
FROM "WoSTestAffiliationStaging";

ANALYZE "WoSTestAffiliation" ;

SELECT CONCAT( 'WoSAffiliationFromStaging staging finishing at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

-- TRUNCATE "WoSTestAffiliationStaging";
