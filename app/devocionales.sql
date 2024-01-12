CREATE TABLE IF NOT EXISTS devocionales (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    semana TEXT,
    titulo_video TEXT,
    video_link TEXT,
    descripcion_video TEXT,
    titulo_audio TEXT,
    descripcion_audio TEXT,
    soundcloud_link TEXT,
    titulo TEXT,
    tema TEXT,
    instrucciones TEXT,
    devocional TEXT,
    reflexion TEXT,
    capitulo TEXT,
    lectura TEXT,
    biografia TEXT,
    trivia_id UUID,
    fecha DATE,
    podcast_id UUID
);

/*EJECUTAR AMBOS DESPUES DE CREAR LA TABLA DEVOCIONALES, TRIVIA Y PODCAST*/
ALTER TABLE devocionales
ADD CONSTRAINT fk_podcast
FOREIGN KEY (podcast_id) REFERENCES podcast(id);

ALTER TABLE devocionales
ADD CONSTRAINT fk_trivia
FOREIGN KEY (trivia_id) REFERENCES trivia(id);