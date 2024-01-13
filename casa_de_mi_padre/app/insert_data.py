import json
from psycopg2 import sql
from datetime import datetime
import uuid  # If you need UUID generation
from db.dbManager import get_db_cursor


def insertar_datos(map):
 with get_db_cursor() as cur:
    map['fecha'] = datetime.now().date()
    
    query = sql.SQL("""
        INSERT INTO devocionales (semana, 
         titulo_video,
         video_link,
         descripcion_video, 
         titulo_audio, 
         descripcion_audio, 
         soundcloud_link, 
         titulo, 
         tema, 
         instrucciones, 
         devocional, 
         reflexion, 
         capitulo, 
         lectura, 
         biografia,
         fecha) 
        VALUES (%(semana)s,
          %(titulo_video)s,
          %(video_link)s, 
          %(descripcion_video)s,
          %(titulo_audio)s, 
          %(descripcion_audio)s,
          %(soundcloud_link)s,
          %(titulo)s,
          %(tema)s,
          %(instrucciones)s, 
          %(devocional)s, 
          %(reflexion)s, 
          %(capitulo)s, 
          %(lectura)s, 
          %(biografia)s,
          %(fecha)s
          ) RETURNING id
    """)

    cur.execute(query, map)

    map['trivia'] = json.dumps(map['trivia'])

    # Después de cur.execute(query, map)
    devocional_id = cur.fetchone()[0]

    map['devocional_id'] = devocional_id

    # Luego, insertar la trivia usando el devocional_id
    trivia_query = sql.SQL("""
    INSERT INTO trivia (devocional_id, trivia, fecha) 
    VALUES (%(devocional_id)s, %(trivia)s, %(fecha)s)
    RETURNING id
    """)

    cur.execute(trivia_query, map)

    trivia_id = cur.fetchone()[0]

    map['trivia_id'] = trivia_id

    # Luego, insertar el id de la trivia en la tabla devocionales
    devocional_trivia_query = sql.SQL("""
    UPDATE devocionales
    SET trivia_id = %(trivia_id)s
    WHERE id = %(devocional_id)s
    """)
    cur.execute(devocional_trivia_query, map)

    # Luego, insertar la trivia usando el devocional_id
    podcast_query = sql.SQL("""
    INSERT INTO podcast (devocional_id, podcast_uri, fecha) 
    VALUES (%(devocional_id)s, %(podcast)s, %(fecha)s)
    RETURNING id
    """)
    cur.execute(podcast_query, map)

    podcast_id = cur.fetchone()[0]

    map['podcast_id'] = podcast_id

    # Luego, insertar el id del podcast en la tabla devocionales
    devocional_podcast_query = sql.SQL("""
    UPDATE devocionales
    SET podcast_id = %(podcast_id)s
    WHERE id = %(devocional_id)s
    """)
    cur.execute(devocional_podcast_query, map)

def generate_unique_uuid(conn):
    while True:
        unique_uuid = uuid.uuid4()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM audio_files WHERE unique_id = %s", (unique_uuid,))
        count = cur.fetchone()[0]
        cur.close()
        if count == 0:
            return unique_uuid
        
def insert_audio_file_data(map, devocional_id):
    with get_db_cursor() as cur:
        map['fecha'] = datetime.now().date()
        map['trivia'] = json.dumps(map['trivia'])

        try:
            # Generate a unique UUID
            unique_id = generate_unique_uuid(cur)

            # Insert data into the 'audio_files' table with the generated UUID
            audio_files_query = sql.SQL("""
                INSERT INTO audio_files (unique_id, devocional_id, date, title, url)
                VALUES (%(unique_id)s, %(devocional_id)s, %(fecha)s, %(title)s, %(url)s)
            """)

            # Add values for the audio_files_query
            map['unique_id'] = unique_id
            map['devocional_id'] = devocional_id  # Reference to the 'devocionales' table
            map['title'] = "Your Audio Title"  # Replace with the actual audio title
            map['url'] = "https://audio-url.com"  # Replace with the actual audio URL

            cur.execute(audio_files_query, map)

            return True

        except Exception as e:
            raise e