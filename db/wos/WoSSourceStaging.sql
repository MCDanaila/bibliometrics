DROP TABLE IF EXISTS "WoSTestSourceStaging";

CREATE TABLE "WoSTestSourceStaging"
(
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
