import psycopg2
import json
from psycopg2 import sql
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get PostgreSQL connection details from environment variables
PG_USER = os.getenv("PGUSER")
PG_PASSWORD = os.getenv("PGPASSWORD")
PG_HOST = os.getenv("PGHOST")
PG_PORT = os.getenv("PGPORT")
PG_DATABASE = os.getenv("PGDATABASE")

def insertar_datos(map):
    # Conexión a la base de datos
    conn = psycopg2.connect(
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT
    )

    cur = conn.cursor()
    
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
    conn.commit()

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
    conn.commit()

    trivia_id = cur.fetchone()[0]

    map['trivia_id'] = trivia_id

    # Luego, insertar el id de la trivia en la tabla devocionales
    devocional_trivia_query = sql.SQL("""
    UPDATE devocionales
    SET trivia_id = %(trivia_id)s
    WHERE id = %(devocional_id)s
    """)
    cur.execute(devocional_trivia_query, map)
    conn.commit()

    cur.close()
    conn.close()
