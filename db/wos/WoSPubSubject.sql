DROP TABLE IF EXISTS "WoSTestPubSubject" ;

CREATE TABLE "WoSTestPubSubject"
(
  pub_id  INTEGER,
  subject VARCHAR
) ;

GRANT SELECT ON TABLE "WoSTestPubSubject" TO "biblio01";
