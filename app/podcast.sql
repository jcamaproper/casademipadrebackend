CREATE TABLE IF NOT EXISTS PODCAST (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    podcast_uri TEXT,
    devocional_id UUID REFERENCES devocionales(id),
    fecha DATE
);