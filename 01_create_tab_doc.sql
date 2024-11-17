CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS doc (
    doc_id SERIAL PRIMARY KEY,
    doc_text varchar(100), 
    doc_vector VECTOR(768) 
);


-- Beispiele für Vektor-Indexe
--CREATE INDEX doc_idx ON docs USING hnsw (doc_vector);

/*
-- Beispielabfragen wenn Tabellen gefuellt sind
SELECT doc_text, doc_vector <-> (SELECT doc_vector FROM docs WHERE doc_id = 1) AS similarity
FROM doc_vector
ORDER BY similarity
LIMIT 5;

*/

