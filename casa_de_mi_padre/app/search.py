from docx import Document
from unidecode import unidecode
from insert_data import insertar_datos
#from firebase import send_push_notifications
from psycopg2.extras import register_uuid
from dotenv import load_dotenv
from db.dbManager import get_db_cursor

# Obtiene los devocionales de la base de datos
# filters: columna por la que se va a filtrar
def obtener_devocionales(filters, offset=0, limite=10):
    with get_db_cursor() as cur:
        # Base de la consulta
        base_query = "SELECT * FROM devocionales WHERE fecha <= CURRENT_DATE"
        count_query = "SELECT COUNT(*) FROM devocionales WHERE fecha <= CURRENT_DATE"

        # Construir cláusulas WHERE para filtrar
        where_clauses = []
        params = []
        for key, value in filters.items():
            where_clauses.append(f"{key} LIKE %s")
            params.append(f"%{value}%")

        # Agregar WHERE a las consultas
        if where_clauses:
            where_clause = " WHERE " + " AND ".join(where_clauses)
            base_query += where_clause
            count_query += where_clause

        # Consulta para contar el total de registros
        cur.execute(count_query, params)
        total_registros = cur.fetchone()[0]

        # Calcular el número total de páginas
        total_paginas = -(-total_registros // limite)

        # Consulta para obtener registros con paginación
        paginated_query = base_query + " ORDER BY fecha DESC OFFSET %s LIMIT %s"
        params.extend([offset, limite])
        cur.execute(paginated_query, params)
        registros = cur.fetchall()

        # Preparar los registros para la respuesta
        columnas = [desc[0] for desc in cur.description]
        devocionales = [dict(zip(columnas, registro)) for registro in registros]

        # Estructurar la respuesta
        respuesta = {
            "status": "success",
            "data": {
                "results": devocionales,
                "count": total_registros,
                "pages": total_paginas
            }
        }
        return respuesta


# Obtener los devocionales por su UUID
def obtener_devocional_por_uuid(devocional_uuid):
    register_uuid()
    # Conexión a la base de datos
    with get_db_cursor() as cur:
        devocional_uuid_str = str(devocional_uuid)
        cur.execute("""
            SELECT * FROM devocionales
            WHERE id = %s
        """, (devocional_uuid_str,))

        registro = cur.fetchone()

        columnas = [desc[0] for desc in cur.description]
        devocional = dict(zip(columnas, registro))
        return devocional

# Obtener las trivias por su UUID
def obtener_trivia_por_uuid(trivia_uuid):
    register_uuid()
    # Conexión a la base de datos
    with get_db_cursor() as cur:
        trivia_uuid_str = str(trivia_uuid)

        cur.execute("""
            SELECT * FROM trivia
            WHERE id = %s
        """, (trivia_uuid_str,))

        registro = cur.fetchone()

        columnas = [desc[0] for desc in cur.description]
        trivia = dict(zip(columnas, registro))
        return trivia

# Obtener los podcasts por su UUID
def obtener_podcast_por_uuid(podcast_uuid):
    register_uuid()
    # Conexión a la base de datos
    with get_db_cursor() as cur:
        podcast_uuid_str = str(podcast_uuid)
        cur.execute("""
            SELECT * FROM podcast
            WHERE id = %s
        """, (podcast_uuid_str,))

        registro = cur.fetchone()

        columnas = [desc[0] for desc in cur.description]
        podcast = dict(zip(columnas, registro))
        return podcast

def obtener_trivias(offset=0, limite=10):
    # Conexión a la base de datos
    with get_db_cursor() as cur:
        # Primero, obtenemos el total de trivias en la base de datos
        cur.execute("SELECT COUNT(*) FROM trivia")
        total_registros = cur.fetchone()[0]

        # Calcular el número total de páginas
        total_paginas = -(-total_registros // limite)  # Redondeo hacia arriba

        # Obtener los registros con paginación
        cur.execute("""
            SELECT * FROM trivia
            WHERE fecha <= CURRENT_DATE
            ORDER BY fecha DESC
            OFFSET %s LIMIT %s
        """, (offset, limite))
        registros = cur.fetchall()

        # Preparar los registros para la respuesta
        columnas = [desc[0] for desc in cur.description]
        trivias = [dict(zip(columnas, registro)) for registro in registros]

        # Estructurar la respuesta
        respuesta = {
            "status": "success",
            "data": {
                "results": trivias,
                "count": total_registros,
                "pages": total_paginas
            }
        }
        return respuesta


def obtener_podcasts(offset=0, limite=10):
    # Conexión a la base de datos
    with get_db_cursor() as cur:
        # Obtener el total de podcasts en la base de datos
        cur.execute("SELECT COUNT(*) FROM podcast")
        total_registros = cur.fetchone()[0]

        # Calcular el número total de páginas
        total_paginas = -(-total_registros // limite)  # Redondeo hacia arriba

        # Obtener los registros con paginación
        cur.execute("""
            SELECT * FROM podcast
            WHERE fecha <= CURRENT_DATE
            ORDER BY fecha DESC
            OFFSET %s LIMIT %s
        """, (offset, limite))
        registros = cur.fetchall()

        # Preparar los registros para la respuesta
        columnas = [desc[0] for desc in cur.description]
        podcasts = [dict(zip(columnas, registro)) for registro in registros]

        # Estructurar la respuesta
        respuesta = {
            "status": "success",
            "data": {
                "results": podcasts,
                "count": total_registros,
                "pages": total_paginas
            }
        }
        return respuesta

def obtener_news(offset=0, limite=10):
    # Conexión a la base de datos
    with get_db_cursor() as cur:
        # Obtener el total de podcasts en la base de datos
        cur.execute("SELECT COUNT(*) FROM news")
        total_registros = cur.fetchone()[0]

        # Calcular el número total de páginas
        total_paginas = -(-total_registros // limite)  # Redondeo hacia arriba

        # Obtener los registros con paginación
        cur.execute("""
            SELECT * FROM news
            ORDER BY fecha DESC
            OFFSET %s LIMIT %s
        """, (offset, limite))
        registros = cur.fetchall()

        # Preparar los registros para la respuesta
        columnas = [desc[0] for desc in cur.description]
        news = [dict(zip(columnas, registro)) for registro in registros]

        # Estructurar la respuesta
        respuesta = {
            "status": "success",
            "data": {
                "results": news,
                "count": total_registros,
                "pages": total_paginas
            }
        }
        return respuesta
    
def obtener_biografias(offset=0, limite=10):
    # Conexión a la base de datos
    with get_db_cursor() as cur:
        # Obtener el total de podcasts en la base de datos
        cur.execute("SELECT COUNT(*) FROM biografias")
        total_registros = cur.fetchone()[0]

        # Calcular el número total de páginas
        total_paginas = -(-total_registros // limite)  # Redondeo hacia arriba

        # Obtener los registros con paginación
        cur.execute("""
            SELECT * FROM biografias
            ORDER BY fecha DESC
            OFFSET %s LIMIT %s
        """, (offset, limite))
        registros = cur.fetchall()

        # Preparar los registros para la respuesta
        columnas = [desc[0] for desc in cur.description]
        biografias = [dict(zip(columnas, registro)) for registro in registros]

        # Estructurar la respuesta
        respuesta = {
            "status": "success",
            "data": {
                "results": biografias,
                "count": total_registros,
                "pages": total_paginas
            }
        }
        return respuesta