import psycopg2
import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate('path/to/google-services.json')
firebase_admin.initialize_app(cred)

conn = psycopg2.connect("dbname=postgres user=postgres password=12345678")
cursor = conn.cursor()

def send_push_notifications():
    # Obtener los tokens de FCM de la tabla usuarios
    cursor.execute("SELECT fcm_token FROM usuarios")
    tokens = [row[0] for row in cursor.fetchall()]

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