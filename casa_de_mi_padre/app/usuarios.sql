CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS usuarios (
    id UUID DEFAULT uuid_generate_v4(),
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL,
    fcm_token VARCHAR(255)
);