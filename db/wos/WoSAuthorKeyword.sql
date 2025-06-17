DROP TABLE IF EXISTS "WoSTestAuthorKeyword" ;

CREATE TABLE "WoSTestAuthorKeyword"
(
  pub_id  INTEGER,
  keyword VARCHAR
) ;

GRANT SELECT ON TABLE "WoSTestAuthorKeyword" TO "biblio01";
