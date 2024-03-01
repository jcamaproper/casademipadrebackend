CREATE TABLE IF NOT EXISTS biografias (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    devocional_id UUID REFERENCES devocionales(id),
    libro TEXT,
    personaje TEXT,
    biografia TEXT,
    fecha DATE
);