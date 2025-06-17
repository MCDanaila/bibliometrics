DROP TABLE IF EXISTS "WoSTestSource";

CREATE TABLE "WoSTestSource"
(
  id            SERIAL        ,
  name          VARCHAR   NULL,
  issn          VARCHAR   NULL,
  abbrev        VARCHAR   NULL,
  publisher     VARCHAR   NULL,
  source_abbrev VARCHAR   NULL,
  abbrev_iso    VARCHAR   NULL,
  abbrev_11     VARCHAR   NULL,
  abbrev_29     VARCHAR   NULL,
  hashval       BIGINT
) ;

GRANT SELECT ON TABLE "WoSTestSource" TO "biblio01";
