DROP TABLE IF EXISTS "ScopusTestZipStatus";

CREATE TABLE "ScopusTestZipStatus"
(
  zip_file_name VARCHAR,
  status        VARCHAR      
);

CREATE INDEX ScopusTest_zip_status_idx ON "ScopusTestZipStatus" (zip_file_name)
