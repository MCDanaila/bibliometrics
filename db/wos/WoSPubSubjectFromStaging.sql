\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true
SELECT CONCAT( 'WoSPubSubjectFromStaging staging starting at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

INSERT INTO "WoSTestPubSubject"
(
  pub_id ,
  subject
)
SELECT p.id, st.subject
FROM   "WoSTestPubSubjectStaging" st,
       "WoSTestPublication"       p
WHERE  st.pub_wos_hash = p.wos_hash ;

ANALYZE  "WoSTestPubSubject" ;

SELECT CONCAT( 'WoSPubSubjectFromStaging staging finishing at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
