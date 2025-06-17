\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true
SELECT CONCAT( 'WoSAuthorFromStaging staging starting at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

INSERT INTO "WoSTestAuthor"
( wos_standard, name, given_name, surname, suffix, e_address, display_name, orcid_id, r_id, hashval)
SELECT 
DISTINCT ON (hashval)
wos_standard, name, given_name, surname, suffix, e_address, display_name, orcid_id, r_id, hashval
FROM "WoSTestAuthorStaging";

ANALYZE "WoSTestAuthor" ;

SELECT CONCAT( 'WoSAuthorFromStaging staging finishing at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

-- TRUNCATE "WoSTestAuthorStaging";
