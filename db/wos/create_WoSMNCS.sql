SELECT publication_year, subject, publication_type, count(*) as publication_count, AVG(citation_count)as mncs
INTO "WoSMNCS"
FROM "WoSPublication", LATERAL UNNEST(ARRAY_CAT(headings, subjects)) AS subject
WHERE publication_year > 2009
      AND is_retracted = 0
      AND subject is not null
GROUP BY publication_year, subject, publication_type
ORDER BY publication_year, subject, publication_type ;
