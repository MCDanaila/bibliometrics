\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true

SELECT CONCAT( 'WoSTestAuthorKeyword_pub_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestAuthorKeyword_pub_id" ON "WoSTestAuthorKeyword" (pub_id) ;

SELECT CONCAT( 'WoSTestAuthorKeyword_keyword index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestAuthorKeyword_keyword" ON "WoSTestAuthorKeyword" (keyword) ;

SELECT CONCAT( 'WoSTestAuthorKeyword post index analyze started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
ANALYZE "WoSTestAuthorKeyword" ;

SELECT CONCAT( 'WoSTestAuthorKeyword index finished at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
