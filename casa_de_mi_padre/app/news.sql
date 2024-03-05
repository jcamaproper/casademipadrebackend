CREATE TABLE IF NOT EXISTS news (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    imagen TEXT,
    titulo TEXT,
    descripcion TEXT,
    fecha DATE
);