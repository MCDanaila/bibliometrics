DROP TABLE IF EXISTS "BibliometricsFileStatus";

CREATE TABLE "BibliometricsFileStatus"
(
  file_name VARCHAR   NOT NULL,
  file_path VARCHAR   NOT NULL,
  provider  VARCHAR   NOT NULL,
  status    VARCHAR   NOT NULL,
  started   TIMESTAMP     NULL,
  finished  TIMESTAMP     NULL
);
