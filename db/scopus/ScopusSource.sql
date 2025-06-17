DROP TABLE IF EXISTS "ScopusTestSource";

CREATE TABLE "ScopusTestSource"
(
  id        BIGINT      ,
  name      VARCHAR     ,
  abbrev    VARCHAR NULL,
  issn      VARCHAR NULL,
  codencode VARCHAR NULL,
  publisher VARCHAR NULL,
  version   CHAR(1)
);

DROP TABLE IF EXISTS "ScopusTestSourceStaging";  -- For uniqueness construction

CREATE TABLE "ScopusTestSourceStaging"
(
  id        BIGINT      ,
  name      VARCHAR     ,
  abbrev    VARCHAR NULL,
  issn      VARCHAR NULL,
  codencode VARCHAR NULL,
  publisher VARCHAR NULL,
  version   CHAR(1)
);
