CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS usuarios (
    id UUID DEFAULT uuid_generate_v4(),
    email TEXT,
    fcm_token VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS fcm_tokens (
    token VARCHAR(255) NOT NULL,
);