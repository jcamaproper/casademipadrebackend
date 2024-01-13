CREATE TABLE IF NOT EXISTS trivia (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    trivia JSONB,
    devocional_id UUID REFERENCES devocionales(id),
    fecha DATE
);