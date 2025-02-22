-- Enable the vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a sample table with a vector column
CREATE TABLE items (
    id bigserial PRIMARY KEY,
    embedding vector(1536),
    metadata jsonb
);

-- Create an index for similarity search
CREATE INDEX ON items USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
