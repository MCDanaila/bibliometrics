SELECT 
    id,
    wos_id,
    publication_year,
    subject,
    citation_count,
    ranking,
    ranking::FLOAT / publication_count AS rank_percentile
INTO "WoSTop10p"
FROM (
    SELECT 
        p.id,
        p.wos_id,
        p.publication_year,
        subject,
        p.citation_count,
        RANK() OVER (PARTITION BY subject, p.publication_year ORDER BY p.citation_count DESC) AS ranking,
        COUNT(*) OVER (PARTITION BY subject, p.publication_year) AS publication_count
    FROM 
        "WoSPublication" p
    JOIN LATERAL UNNEST(p.subjects) AS subject ON true
    WHERE 
        subject IS NOT NULL
        AND p.publication_year > 2009
        AND p.publication_type = 'article'
) subquery
WHERE 
    ranking <= publication_count * 0.1 ;
