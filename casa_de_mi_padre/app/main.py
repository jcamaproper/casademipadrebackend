from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from casa_de_mi_padre.db.dbManager import get_db_cursor
from casa_de_mi_padre.app.read_file import analizar_documento, obtener_devocionales
if __name__ == '__main__':
    from mocks import respuestas_mocks

from bucket_audio_files import upload_audio_to_bucket
import os


app = Flask(__name__)
api = Api(app)

# Retorna el contenido del archivo
class Devocional(Resource):
    def get(self):
        resp = analizar_documento(r'casa_de_mi_padre/app/template4.docx')
        return jsonify(resp)
    
# Retorna los devocionales que hay en la base de datos
class Datos(Resource):
    def get(self):
        page = request.args.get('page', default = 1, type = int)
        per_page = request.args.get('per_page', default = 10, type = int)
        resp = obtener_devocionales(page, per_page)
        return jsonify(resp)

# Retorna los datos de prueba (52 semanas)
class Mocks(Resource):
    def get(self):
        page = request.args.get('page', default = 1, type = int)
        per_page = request.args.get('per_page', default = 10, type = int)
        resp = respuestas_mocks(page, per_page)
        return jsonify(resp)
    
class AudioUploadResource(Resource):
    def post(self):
        try:
            print('estoy aqui')
            audio_file = request.files['audio_file']

            if audio_file:
                # Upload the audio file to Google Cloud Storage
                file_url = upload_audio_to_bucket(audio_file,'casademipadredevo')

                # Optionally, save the URL to your PostgreSQL database here

                return {'message': 'Audio file uploaded successfully', 'file_url': file_url}, 200
            else:
                return {'message': 'No audio file provided'}, 400
        except Exception as e:
            return {'message': 'An error occurred', 'error': str(e)}, 500
        


api.add_resource(Devocional, '/devocional')
api.add_resource(Mocks, '/mocks')
api.add_resource(Datos, '/datos')
api.add_resource(AudioUploadResource, '/upload-audio')

if __name__ == '__main__':
    app.run(debug=True)
