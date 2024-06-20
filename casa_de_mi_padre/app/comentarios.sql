CREATE TABLE IF NOT EXISTS comentarios (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    devocional_id UUID,
    podcast_id UUID,
    usuario_id UUID,
    comentario_id UUID, -- Para almacenar el ID del comentario al que se está respondiendo
    comentario TEXT NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (comentario_id) REFERENCES comentarios(id) -- Clave foránea autoreferencial para las respuestas
);
