CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS music (
   id INTEGER PRIMARY KEY,
   artistname VARCHAR(250),
   songname VARCHAR(250),
   songvector VECTOR(4) 
);
