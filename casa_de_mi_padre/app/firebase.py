import psycopg2
import firebase_admin
from firebase_admin import credentials, messaging
from db.dbManager import get_db_cursor
import os
from datetime import datetime


# Use the FIREBASE_APPLICATION_CREDENTIALS environment variable
cred = credentials.Certificate(os.environ.get('FIREBASE_APPLICATION_CREDENTIALS'))
firebase_admin.initialize_app(cred)

def send_push_notifications(message_title, message_body):
    with get_db_cursor() as cur:
        # Obtener los tokens de FCM de la tabla usuarios
        cur.execute("SELECT token FROM fcm_tokens")
        tokens = [row[0] for row in cur.fetchall()]

        # Split the tokens into chunks of 500
        def split_into_chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        token_chunks = list(split_into_chunks(tokens, 500))

        # Notification details
        image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTFslxyzQviWRDupowqMiCYeDfu6IFZughPIOnkAHo6mQ&s"

        total_sent = 0

        for chunk in token_chunks:
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=message_title,
                    body=message_body,
                    image=image_url
                ),
                tokens=chunk,
            )

            # Enviar notificación
            response = messaging.send_multicast(message)
            total_sent += response.success_count
            print(f'Mensajes enviados en este lote: {response.success_count} / {len(chunk)}')

        print(f'Total mensajes enviados: {total_sent} / {len(tokens)}')

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

def send_devotional_push_notification():
    today_date = datetime.now().strftime('%Y-%m-%d')
    format_date = datetime.now().strftime('%d de %B de %Y')
    with get_db_cursor() as cur:
        cur.execute("SELECT titulo, tema FROM devocionales WHERE fecha = %s", (today_date,))
        devotional = cur.fetchone()
        if devotional:
            titulo, tema = devotional
            # Use titulo and tema in your message or modify message_title and message_body as needed
            custom_message_title = "Los 365 capítulos más importantes de la Biblia"
            custom_message_body = f"Hay un nuevo devocional para ti {tema} - {format_date}"
            # If there's a devotional for today, proceed to send push notifications with the custom title and body
            send_push_notifications(custom_message_title, custom_message_body)
            print(f"Push notification sent for devotional on {today_date} with title '{titulo}' and tema '{tema}'.")
        else:
            print(f"No devotional found for {today_date}, no push notification sent.")