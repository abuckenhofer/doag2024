DROP INDEX IF EXISTS music_ivf;
DROP INDEX IF EXISTS music_hnsw;

CREATE INDEX music_hnsw ON music 
       USING hnsw (songVector vector_cosine_ops) 
       WITH (m = 16, ef_construction = 200);