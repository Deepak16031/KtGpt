CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS problems
(
    id UUID PRIMARY
        KEY
        DEFAULT
        uuid_generate_v4
        (
        ),
    title       VARCHAR(255) NOT NULL,
    description TEXT         NOT NULL,
    solution    TEXT         NOT NULL,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS code_snippets
(
    id
        UUID
        PRIMARY
        KEY
        DEFAULT
        uuid_generate_v4
        (
        ),
    problem_id UUID REFERENCES problems
        (
        id
        ) ON DELETE CASCADE,
    language   VARCHAR(50) NOT NULL,
    content    TEXT        NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS problem_tags
(
    problem_id
        UUID
        REFERENCES
        problems
        (
        id
        ) ON DELETE CASCADE,
    tag VARCHAR(100) NOT NULL,
    PRIMARY KEY
        (
         problem_id,
         tag
            )
);

CREATE TABLE IF NOT EXISTS embeddings
(
    problem_id
        UUID
        PRIMARY
        KEY
        REFERENCES
        problems
        (
        id
        ) ON DELETE CASCADE,
    embedding vector(384) NOT NULL
);