\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true

SELECT CONCAT( 'WoSTestCitation_ed_ing index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestCitation_ed_ing" ON "WoSTestCitation" ( referenced_id, referencing_id) ;

SELECT CONCAT( 'WoSTestCitation_ing_ed index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestCitation_ing_ed" ON "WoSTestCitation" ( referencing_id, referenced_id) ;

SELECT CONCAT( 'WoSTestCitation post index analyze started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
ANALYZE "WoSTestCitation" ;

SELECT CONCAT( 'WoSTestCitation index finished at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
