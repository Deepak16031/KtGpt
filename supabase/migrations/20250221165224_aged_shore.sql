/*
  # Initial Schema Setup for DevKnowledge

  1. New Tables
    - `problems`
      - `id` (uuid, primary key)
      - `title` (text)
      - `description` (text)
      - `solution` (text)
      - `created_at` (timestamp)
      - `updated_at` (timestamp)
    
    - `code_snippets`
      - `id` (uuid, primary key)
      - `problem_id` (uuid, foreign key)
      - `language` (text)
      - `code` (text)
      - `created_at` (timestamp)
    
    - `problem_tags`
      - `problem_id` (uuid, foreign key)
      - `tag` (text)
    
    - `embeddings`
      - `id` (uuid, primary key)
      - `problem_id` (uuid, foreign key)
      - `embedding` (vector)
      - `created_at` (timestamp)

  2. Security
    - Enable RLS on all tables
    - Add policies for full access (single user mode)
*/

-- Enable pgvector extension for embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Problems table
CREATE TABLE IF NOT EXISTS problems (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    title text NOT NULL,
    description text NOT NULL,
    solution text NOT NULL,
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);

-- Code snippets table
CREATE TABLE IF NOT EXISTS code_snippets (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    problem_id uuid REFERENCES problems(id) ON DELETE CASCADE,
    language text NOT NULL,
    code text NOT NULL,
    created_at timestamptz DEFAULT now()
);

-- Problem tags table
CREATE TABLE IF NOT EXISTS problem_tags (
    problem_id uuid REFERENCES problems(id) ON DELETE CASCADE,
    tag text NOT NULL,
    created_at timestamptz DEFAULT now(),
    PRIMARY KEY (problem_id, tag)
);

-- Embeddings table for semantic search
CREATE TABLE IF NOT EXISTS embeddings (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    problem_id uuid REFERENCES problems(id) ON DELETE CASCADE,
    embedding vector(384),
    created_at timestamptz DEFAULT now()
);

-- Enable RLS
ALTER TABLE problems ENABLE ROW LEVEL SECURITY;
ALTER TABLE code_snippets ENABLE ROW LEVEL SECURITY;
ALTER TABLE problem_tags ENABLE ROW LEVEL SECURITY;
ALTER TABLE embeddings ENABLE ROW LEVEL SECURITY;

-- Create policies (single user mode, so we allow all operations)
CREATE POLICY "Allow all operations on problems"
    ON problems
    FOR ALL
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Allow all operations on code_snippets"
    ON code_snippets
    FOR ALL
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Allow all operations on problem_tags"
    ON problem_tags
    FOR ALL
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Allow all operations on embeddings"
    ON embeddings
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_problems_updated_at
    BEFORE UPDATE ON problems
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();