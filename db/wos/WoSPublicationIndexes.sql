\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true

SELECT CONCAT( 'WoSTestPublication_wos_id_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE UNIQUE INDEX "WoSTestPublication_wos_id_id" ON "WoSTestPublication" (wos_id, id) ;

/* Not needed since done after creation from staging - 
   maybe all main indices should be done there. Or maybe this script should be run there. AMB 23.11.24
SELECT CONCAT( 'WoSTestPublication_wos_hash_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE UNIQUE INDEX "WoSTestPublication_wos_hash_id" ON "WoSTestPublication" (wos_hash, id) ;
*/

SELECT CONCAT( 'WoSTestPublication_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
SELECT CONCAT( 'WoSTestPublication_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE UNIQUE INDEX "WoSTestPublication_id" ON "WoSTestPublication" (id) ;

SELECT CONCAT( 'WoSTestPublication_doi_index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestPublication_doi" ON "WoSTestPublication" ( doi) ;    -- turns out doi are not unique

SELECT CONCAT( 'WoSTestPublication_year_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestPublication_year_id"  ON "WoSTestPublication" (publication_year, id) ;

SELECT CONCAT( 'WoSTestPublication_headings index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestPublication_headings" ON "WoSTestPublication" (headings, id) ; /* Not sure if this is useful */

SELECT CONCAT( 'WoSTestPublication_publication_type_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestPublication_publication_type_id"  ON "WoSTestPublication" (publication_type, id) ;

SELECT CONCAT( 'WoSTestPublication_wos_publication_type_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestPublication_wos_wos_publication_type_id"  ON "WoSTestPublication" (wos_publication_type, id) ;

SELECT CONCAT( 'WoSTestPublication_is_retracted_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestPublication_is_retracted_id"  ON "WoSTestPublication" (is_retracted, id) ;

SELECT CONCAT( 'WoSTestPublication_subjects_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestPublication_subjects_id"  ON "WoSTestPublication" (subjects, id) ;

SELECT CONCAT( 'WoSTestPublication_source_id index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestPublication_source_id" ON "WoSTestPublication" ( source_id) ;

SELECT CONCAT( 'WoSTestPublication_title index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSTestPublication_title" ON "WoSTestPublication" ( title) ;

SELECT CONCAT( 'WoSTestPublication ANALYZE post index analyze started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
ANALYZE "WoSTestPublication" ; 

SELECT CONCAT( 'WoSTestPublication indexes finished at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
