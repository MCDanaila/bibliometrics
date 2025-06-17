SELECT DISTINCT subject, heading
INTO "WoSFieldResearch"
FROM (
    SELECT UNNEST(subjects) AS subject, headings[1] AS heading
    FROM "WoSPublication"
	WHERE array_length(headings, 1) = 1
) AS unnested_data
ORDER BY heading;


\o /dev/null
SET client_min_messages TO WARNING;
\o
\pset tuples_only true

SELECT CONCAT( 'WoSFieldResearch_heading index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSFieldResearch_heading" ON "WoSFieldResearch" (heading) ;

SELECT CONCAT( 'WoSFieldResearch_subject index create started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
CREATE INDEX "WoSFieldResearch_subject" ON "WoSFieldResearch" (subject) ;

SELECT CONCAT( 'WoSFieldResearch post index analyze started at ', to_char( NOW(), 'DD HH24:MI:SS')) ;
ANALYZE "WoSFieldResearch" ;

SELECT CONCAT( 'WoSFieldResearch index finished at ', to_char( NOW(), 'DD HH24:MI:SS')) ;

/* 
-- Table: bibliometrics_s1.WoSFieldResearch

-- DROP TABLE IF EXISTS bibliometrics_s1."WoSFieldResearch";

CREATE TABLE IF NOT EXISTS bibliometrics_s1."WoSFieldResearch"
(
    subject character varying COLLATE pg_catalog."default",
    heading character varying COLLATE pg_catalog."default"
)

TABLESPACE bibliometrics_ts1;

ALTER TABLE IF EXISTS bibliometrics_s1."WoSFieldResearch"
    OWNER to biblioowner;

REVOKE ALL ON TABLE bibliometrics_s1."WoSFieldResearch" FROM biblio01;
REVOKE ALL ON TABLE bibliometrics_s1."WoSFieldResearch" FROM biblioguest;

GRANT SELECT ON TABLE bibliometrics_s1."WoSFieldResearch" TO biblio01;

GRANT SELECT ON TABLE bibliometrics_s1."WoSFieldResearch" TO biblioguest;

GRANT ALL ON TABLE bibliometrics_s1."WoSFieldResearch" TO biblioowner;
-- Index: WoSFieldResearch_heading

-- DROP INDEX IF EXISTS bibliometrics_s1."WoSFieldResearch_heading";

CREATE INDEX IF NOT EXISTS "WoSFieldResearch_heading"
    ON bibliometrics_s1."WoSFieldResearch" USING btree
    (heading COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE bibliometrics_ts1;
-- Index: WoSFieldResearch_subject

-- DROP INDEX IF EXISTS bibliometrics_s1."WoSFieldResearch_subject";

CREATE INDEX IF NOT EXISTS "WoSFieldResearch_subject"
    ON bibliometrics_s1."WoSFieldResearch" USING btree
    (subject COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE bibliometrics_ts1;
*/` 