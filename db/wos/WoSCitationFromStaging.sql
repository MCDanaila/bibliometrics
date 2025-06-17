\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true
SELECT CONCAT( 'WoSCitationFromStaging staging starting at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

DROP   INDEX IF EXISTS "WoSTestCitationStaging_ed_ing"                                                                          ;
CREATE INDEX           "WoSTestCitationStaging_ed_ing" ON "WoSTestCitationStaging" ( referenced_pub_hash, referencing_pub_hash) ;
DROP   INDEX IF EXISTS "WoSTestCitationStaging_ing_ed"                                                                          ;
CREATE INDEX           "WoSTestCitationStaging_ing_ed" ON "WoSTestCitationStaging" ( referencing_pub_hash, referenced_pub_hash) ;

INSERT INTO "WoSTestCitation"
(
  referencing_id,
  referenced_id
)
SELECT referencing.id, referenced.id
FROM   "WoSTestCitationStaging" st         ,
       "WoSTestPublication"     referencing,
       "WoSTestPublication"     referenced
WHERE  st.referencing_pub_hash = referencing.wos_hash
AND    st.referenced_pub_hash  = referenced.wos_hash ;

SELECT CONCAT( 'WoSCitationFromStaging staging finishing at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
