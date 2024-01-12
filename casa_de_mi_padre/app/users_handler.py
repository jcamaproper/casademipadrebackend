from flask import Flask, request
import psycopg2

app = Flask(__name__)

@app.route('/update_token', methods=['POST'])
def update_token():
    user_id = request.json.get('user_id')
    token = request.json.get('token')

    # Aquí, actualiza el token en tu base de datos
    conn = psycopg2.connect("dbname=postgres user=postgres password=12345678")
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET fcm_token = %s WHERE id = %s", (token, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    return "Token actualizado", 200

if __name__ == '__main__':
    app.run(debug=True)
