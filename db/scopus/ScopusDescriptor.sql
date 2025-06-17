DROP TABLE IF EXISTS "ScopusTestDescriptor" ;

CREATE TABLE "ScopusTestDescriptor"
(
  pub_id          BIGINT      ,
  descriptor_type VARCHAR     ,
  description     VARCHAR     ,
  weight          CHAR(1) NULL,
  controlled      CHAR(1) NULL,
  candidate       CHAR(1) NULL,
  version         CHAR(1)
) ;
