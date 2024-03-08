import psycopg2
import firebase_admin
from firebase_admin import credentials, messaging
from db.dbManager import get_db_cursor
import os

# Use the FIREBASE_APPLICATION_CREDENTIALS environment variable
cred = credentials.Certificate(os.environ.get('FIREBASE_APPLICATION_CREDENTIALS'))
firebase_admin.initialize_app(cred)

def send_push_notifications():
    with get_db_cursor() as cur:
        # Obtener los tokens de FCM de la tabla usuarios
        cur.execute("SELECT token FROM fcm_tokens")
        tokens = [row[0] for row in cur.fetchall()]

        # Crear y enviar notificaciones
        for token in tokens:
            message = messaging.Message(
                notification=messaging.Notification(
                    title='Nuevo Devocional',
                    body='Se ha añadido un nuevo devocional.'
                ),
                token=token,
            )
            response = messaging.send(message)
            print('Mensaje enviado:', response)

def upsert_users_and_tokens(email=None, token=None):
    with get_db_cursor() as cur:
        try:
            token_insert_query = """
            INSERT INTO fcm_tokens (token) VALUES (%s)
            """
            cur.execute(token_insert_query, (token,))

            if email:
                user_upsert_query = """
                INSERT INTO usuarios (email, token) VALUES (%s, %s)
                """
                cur.execute(user_upsert_query, (email,token))

            return "Operation completed successfully", 200

        except Exception as e:
            raise e
