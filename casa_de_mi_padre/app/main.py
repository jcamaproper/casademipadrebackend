from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from db.dbManager import get_db_cursor
from app.read_file import analizar_documento
from app.search import obtener_devocionales, obtener_trivias, obtener_podcasts, obtener_podcast_por_uuid, obtener_trivia_por_uuid, obtener_devocional_por_uuid
import uuid

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
    
class Devocionales(Resource):
    def get(self):
        page = request.args.get('page', default=0, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        filters = {key: value for key, value in request.args.items() if key not in ['page', 'per_page']}
        resp = obtener_devocionales(filters, (page - 1) * per_page, per_page)
        return jsonify(resp)

# Retorna los datos de prueba (52 semanas)
class Mocks(Resource):
    def get(self):
        page = request.args.get('page', default = 0, type = int)
        per_page = request.args.get('per_page', default = 10, type = int)
        resp = respuestas_mocks(page, per_page)
        return jsonify(resp)
    
# Retorna las trivias que hay en la base de datos
class Trivia(Resource):
    def get(self):
        page = request.args.get('page', default = 0, type = int)
        per_page = request.args.get('per_page', default = 10, type = int)
        resp = obtener_trivias(page, per_page)
        return jsonify(resp)
# Retorna los podcasts que hay en la base de datos
class Podcast(Resource):
    def get(self):
        page = request.args.get('page', default = 0, type = int)
        per_page = request.args.get('per_page', default = 10, type = int)
        resp = obtener_podcasts(page, per_page)
        return jsonify(resp)
# Retorna un podcast por su UUID

class PodcastById(Resource):
    def get(self, podcast_id):
        try:
            podcast_uuid = uuid.UUID(podcast_id)
            resp = obtener_podcast_por_uuid(podcast_uuid)
            return jsonify(resp)
        except ValueError:
            return "Invalid UUID", 400
        
# Retorna una trivia por su UUID
class TriviaById(Resource):
    def get(self, trivia_id):
        try:
            trivia_uuid = uuid.UUID(trivia_id)
            resp = obtener_trivia_por_uuid(trivia_uuid)
            return jsonify(resp)
        except ValueError:
            return "Invalid UUID", 400

# Retorna un devocional por su UUID
class DevocionalById(Resource):
    def get(self, devocional_id):
        try:
            devocional_uuid = uuid.UUID(devocional_id)
            resp = obtener_devocional_por_uuid(devocional_uuid)
            return jsonify(resp)
        except ValueError:
            return "Invalid UUID", 400
        
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
        


api.add_resource(AudioUploadResource, '/upload-audio')
api.add_resource(Devocional, '/devocional')
api.add_resource(Mocks, '/mocks')
api.add_resource(Devocionales, '/devocionales-list')
api.add_resource(Trivia, '/trivia-list')
api.add_resource(Podcast, '/podcast-list')
api.add_resource(PodcastById, '/podcast/<string:podcast_id>')
api.add_resource(TriviaById, '/trivia/<string:trivia_id>')
api.add_resource(DevocionalById, '/devocional/<string:devocional_id>')

def run_app():
    # Set port to 10000 for Render, default to 5000 for local development
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    run_app()