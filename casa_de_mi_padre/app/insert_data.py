import json
from psycopg2 import sql
from datetime import datetime
import uuid  # If you need UUID generation
from db.dbManager import get_db_cursor
import re
from app.firebase import send_push_notifications


def insertar_datos(map):
 with get_db_cursor() as cur:
    map['fecha'] = extract_and_convert_date(map['titulo'])
    
    # Check if there is an existing devocional with the same fecha
    cur.execute("SELECT COUNT(*) FROM devocionales WHERE fecha = %s", (map['fecha'],))
    if cur.fetchone()[0] > 0:
        return "already exist"
    
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

    if map.get('trivia') and map['trivia'] != '{}':
        trivia_query = sql.SQL("""
        INSERT INTO trivia (devocional_id, trivia, fecha, semana) 
        VALUES (%(devocional_id)s, %(trivia)s, %(fecha)s, %(semana)s)
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
    INSERT INTO podcast (devocional_id, podcast_uri, fecha, tema, descripcion) 
    VALUES (%(devocional_id)s, %(podcast)s, %(fecha)s, %(tema)s, %(descripcion_audio)s)
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

    if map.get('libro') and map['libro'] != '':
        biografia_query = sql.SQL("""
        INSERT INTO biografias (devocional_id, libro, personaje, biografia, fecha) 
        VALUES (%(devocional_id)s, %(libro)s, %(personaje)s, %(texto)s, %(fecha)s)
        RETURNING id
        """)
        cur.execute(biografia_query, map)

        biografia_id = cur.fetchone()[0]

        map['biografia_id'] = biografia_id

        # Luego, insertar el id del podcast en la tabla devocionales
        devocional_biografia_query = sql.SQL("""
        UPDATE devocionales
        SET biografia_id = %(biografia_id)s
        WHERE id = %(devocional_id)s
        """)
        cur.execute(devocional_biografia_query, map)

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
        

def extract_and_convert_date(text):
    # Diccionario para mapear nombres de meses en español a inglés
    months_es_to_en = {
        'enero': 'January',
        'febrero': 'February',
        'marzo': 'March',
        'abril': 'April',
        'mayo': 'May',
        'junio': 'June',
        'julio': 'July',
        'agosto': 'August',
        'septiembre': 'September',
        'octubre': 'October',
        'noviembre': 'November',
        'diciembre': 'December'
    }

    # Extraer la fecha usando expresión regular
    match = re.search(r'(\d{1,2}) de (enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre) de (\d{4})', text)
    if match:
        day, month_es, year = match.groups()
        month_en = months_es_to_en[month_es.lower()]
        date_str = f'{day} {month_en} {year}'

        # Convertir la cadena de fecha a un objeto datetime
        date_obj = datetime.strptime(date_str, '%d %B %Y')

        # date_obj es ahora un objeto datetime representando la fecha
        return date_obj
        #print(date_obj)
    else:
        return datetime.now().date()

def insert_news(image_url, title, description):
    with get_db_cursor() as cur:
        map = {}
        map['fecha'] = datetime.now().date()
        map['titulo'] = title
        map['descripcion'] = description
        map['imagen'] = image_url

        try:
            query = sql.SQL("""
            INSERT INTO news (titulo, descripcion, imagen, fecha) 
            VALUES (%(titulo)s, %(descripcion)s, %(imagen)s, %(fecha)s)
            RETURNING id
            """)
            cur.execute(query, map)
            send_push_notifications(title, description)
            return True

        except Exception as e:
            raise e
        
def insert_comment(devotional_id, podcast_id, user_id, comment):
    with get_db_cursor() as cur:
        map = {}
        map['devocional_id'] = devotional_id if devotional_id else None
        map['podcast_id'] = podcast_id if podcast_id else None
        map['user_id'] = user_id
        map['comentario'] = comment

        try:
            query = sql.SQL("""
            INSERT INTO comentarios (devocional_id, podcast_id, usuario_id, comentario) 
            VALUES (%(devocional_id)s, %(podcast_id)s, %(user_id)s, %(comentario)s)
            RETURNING id
            """)
            cur.execute(query, map)
            return

        except Exception as e:
            raise e
        

def insert_comment_reply(devotional_id, podcast_id, user_id, comment_id, comment):
    with get_db_cursor() as cur:
        map = {}
        map['devocional_id'] = devotional_id if devotional_id else None
        map['podcast_id'] = podcast_id if podcast_id else None
        map['user_id'] = user_id
        map['comentario_id'] = comment_id
        map['comentario'] = comment

        try:
            query = sql.SQL("""
            INSERT INTO comentarios (devocional_id, podcast_id, usuario_id, comentario_id, comentario) 
            VALUES (%(devocional_id)s, %(podcast_id)s, %(user_id)s, %(comentario_id)s, %(comentario)s)
            RETURNING id
            """)
            cur.execute(query, map)
            return True

        except Exception as e:
            raise e
         
def delete_comment(comment_id):
    with get_db_cursor() as cur:
        try:
            # First, delete child comments
            query = sql.SQL("""
            DELETE FROM comentarios WHERE comentario_id = %s
            """)
            cur.execute(query, (comment_id,))

            # Then, delete the parent comment
            query = sql.SQL("""
            DELETE FROM comentarios WHERE id = %s
            """)
            cur.execute(query, (comment_id,))

            return

        except Exception as e:
            return {
                "message": "An error occurred",
                "error": str(e)
            }