DROP TABLE IF EXISTS "WoSTestAuthorStaging";

CREATE TABLE "WoSTestAuthorStaging"
(
  wos_standard VARCHAR       ,
  name         VARCHAR   NULL,
  given_name   VARCHAR   NULL,
  surname      VARCHAR   NULL,
  suffix       VARCHAR   NULL,
  e_address    VARCHAR   NULL,
  display_name VARCHAR   NULL,
  orcid_id     VARCHAR   NULL,
  r_id         VARCHAR   NULL,
  hashval      BIGINT
);
