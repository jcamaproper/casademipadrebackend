from docx import Document
from unidecode import unidecode
from insert import insertar_datos
#from firebase import send_push_notifications
import psycopg2
from psycopg2.extras import register_uuid
import os
from dotenv import load_dotenv

# Get PostgreSQL connection details from environment variables
PG_USER = os.getenv("PGUSER")
PG_PASSWORD = os.getenv("PGPASSWORD")
PG_HOST = os.getenv("PGHOST")
PG_PORT = os.getenv("PGPORT")
PG_DATABASE = os.getenv("PGDATABASE")

# Obtiene los devocionales de la base de datos
# filters: columna por la que se va a filtrar
def obtener_devocionales(filters, offset=0, limite=10):
    # Conexión a la base de datos
    conn = psycopg2.connect(
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT
    )

    cur = conn.cursor()

    query = "SELECT * FROM devocionales"

    where_clauses = []
    params = []
    for key, value in filters.items():
        where_clauses.append(f"{key} LIKE %s")
        params.append(f"%{value}%")

    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    query += " ORDER BY fecha DESC OFFSET %s LIMIT %s"

    params.extend([offset, limite])
    cur.execute(query, params)

    registros = cur.fetchall()

    columnas = [desc[0] for desc in cur.description]
    devocionales = []
    for registro in registros:
        devocionales.append(dict(zip(columnas, registro)))

    cur.close()
    conn.close()

    return devocionales

# Obtener los devocionales por su UUID
def obtener_devocional_por_uuid(devocional_uuid):
    register_uuid()
    # Conexión a la base de datos
    conn = psycopg2.connect(
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT
    )

    cur = conn.cursor()

    devocional_uuid_str = str(devocional_uuid)

    cur.execute("""
        SELECT * FROM devocionales
        WHERE id = %s
    """, (devocional_uuid_str,))

    registro = cur.fetchone()

    columnas = [desc[0] for desc in cur.description]
    devocional = dict(zip(columnas, registro))

    cur.close()
    conn.close()

    return devocional

# Obtener las trivias por su UUID
def obtener_trivia_por_uuid(trivia_uuid):
    register_uuid()
    # Conexión a la base de datos
    conn = psycopg2.connect(
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT
    )

    cur = conn.cursor()

    trivia_uuid_str = str(trivia_uuid)

    cur.execute("""
        SELECT * FROM trivia
        WHERE id = %s
    """, (trivia_uuid_str,))

    registro = cur.fetchone()

    columnas = [desc[0] for desc in cur.description]
    trivia = dict(zip(columnas, registro))

    cur.close()
    conn.close()

    return trivia

# Obtener los podcasts por su UUID
def obtener_podcast_por_uuid(podcast_uuid):
    register_uuid()
    # Conexión a la base de datos
    conn = psycopg2.connect(
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT
    )

    cur = conn.cursor()

    podcast_uuid_str = str(podcast_uuid)

    cur.execute("""
        SELECT * FROM podcast
        WHERE id = %s
    """, (podcast_uuid_str,))

    registro = cur.fetchone()

    columnas = [desc[0] for desc in cur.description]
    podcast = dict(zip(columnas, registro))

    cur.close()
    conn.close()

    return podcast

# Obtiene las trivias de la base de datos
def obtener_trivias(offset=0, limite=10):
    # Conexión a la base de datos
    conn = psycopg2.connect(
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT
    )

    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM trivia
        ORDER BY fecha DESC
        OFFSET %s LIMIT %s
    """, (offset, limite))

    registros = cur.fetchall()

    columnas = [desc[0] for desc in cur.description]
    trivias = []
    for registro in registros:
        trivias.append(dict(zip(columnas, registro)))

    cur.close()
    conn.close()

    return trivias

# Obtiene los podcasts de la base de datos
def obtener_podcasts(offset=0, limite=10):
    # Conexión a la base de datos
    conn = psycopg2.connect(
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT
    )

    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM podcast
        ORDER BY fecha DESC
        OFFSET %s LIMIT %s
    """, (offset, limite))

    registros = cur.fetchall()

    columnas = [desc[0] for desc in cur.description]
    podcasts = []
    for registro in registros:
        podcasts.append(dict(zip(columnas, registro)))

    cur.close()
    conn.close()

    return podcasts