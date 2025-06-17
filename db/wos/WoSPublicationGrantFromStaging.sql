\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true
SELECT CONCAT( 'WoSPublicationGrantFromStaging staging starting at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

DROP INDEX IF EXISTS wosTest_publication_grant_staging_hash ;
DROP INDEX IF EXISTS wosTest_grant_hashval                  ;

CREATE INDEX wosTest_publication_grant_staging_hash ON "WoSTestPublicationGrantStaging" ( grant_hash) ;
CREATE INDEX wosTest_grant_hashval                  ON "WoSTestGrant"                   ( hashval   ) ;

ANALYZE "WoSTestPublicationGrantStaging" ;
ANALYZE "WoSTestGrant"                   ;

SELECT CONCAT( 'WoSPublicationGrantFromStaging staging post indices at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

INSERT INTO "WoSTestPublicationGrant"
(
  pub_id  ,
  grant_id
)
SELECT p.id, gr.id
FROM   "WoSTestPublicationGrantStaging" st,
       "WoSTestPublication"             p ,
       "WoSTestGrant"                   gr
WHERE  gr.hashval      = st.grant_hash
AND    st.pub_wos_hash = p.wos_hash ;

ANALYZE  "WoSTestPublicationGrant" ;

SELECT CONCAT( 'WoSPublicationGrantFromStaging staging finishing at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
