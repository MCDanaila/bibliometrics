\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true

SELECT CONCAT( 'WoSTestAuthor_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestAuthor_id" ON "WoSTestAuthor" (id) ;

SELECT CONCAT( 'WoSTestAuthor_wos_standard index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestAuthor_wos_standard" ON "WoSTestAuthor" (wos_standard) ;

SELECT CONCAT( 'WoSTestAuthor_given_name index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestAuthor_given_name" ON "WoSTestAuthor" (given_name) ;

SELECT CONCAT( 'WoSTestAuthor_display_name index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestAuthor_display_name" ON "WoSTestAuthor" (display_name) ;

SELECT CONCAT( 'WoSTestAuthor_orcid_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestAuthor_orcid_id" ON "WoSTestAuthor" (orcid_id) ;

SELECT CONCAT( 'WoSTestAuthor_r_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestAuthor_r_id" ON "WoSTestAuthor" (r_id) ;

SELECT CONCAT( 'WoSTestAuthor post index analyze started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
ANALYZE "WoSTestAuthor" ;

SELECT CONCAT( 'WoSTestAuthor index finished at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
