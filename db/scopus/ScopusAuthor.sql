DROP TABLE IF EXISTS "ScopusTestAuthor";

CREATE TABLE "ScopusTestAuthor"
(
  id             SERIAL      ,
  scopus_id      BIGINT      ,
  degrees        VARCHAR NULL,
  given_name     VARCHAR NULL,
  surname        VARCHAR NULL,
  indexed_name   VARCHAR NULL,
  preferred_name VARCHAR NULL,
  e_address      VARCHAR NULL,
  hashval        VARCHAR     ,
  version        CHAR(1)
);

DROP TABLE IF EXISTS "ScopusTestAuthorStaging";

CREATE TABLE "ScopusTestAuthorStaging"
(
  scopus_id      BIGINT      ,
  degrees        VARCHAR NULL,
  given_name     VARCHAR NULL,
  surname        VARCHAR NULL,
  indexed_name   VARCHAR NULL,
  preferred_name VARCHAR NULL,
  e_address      VARCHAR NULL,
  hashval        VARCHAR     ,
  version        CHAR(1)
);
