SELECT DISTINCT subject, heading
INTO "WoSFieldResearch"
FROM (
    SELECT UNNEST(subjects) AS subject, headings[1] AS heading
    FROM "WoSPublication"
	WHERE array_length(headings, 1) = 1
) AS unnested_data
ORDER BY heading;
