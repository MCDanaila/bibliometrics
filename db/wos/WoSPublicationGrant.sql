DROP TABLE IF EXISTS "WoSTestPublicationGrant";

CREATE TABLE "WoSTestPublicationGrant"
(
  pub_id    INTEGER,
  grant_id  BIGINT
) ;

GRANT SELECT ON TABLE "WoSTestPublicationGrant" TO "biblio01";
