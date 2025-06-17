DROP TABLE IF EXISTS "WoSTestGrant";

CREATE TABLE "WoSTestGrant"
(
  id             SERIAL   ,
  grant_agencies VARCHAR[],
  grant_ids      VARCHAR[],
  hashval        BIGINT
) ;

GRANT SELECT ON TABLE "WoSTestGrant" TO "biblio01";
