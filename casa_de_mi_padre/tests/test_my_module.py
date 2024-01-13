import unittest
from flask import Flask
from casa_de_mi_padre.app.main import app  # Import your Flask app
import io
from werkzeug.datastructures import FileStorage
import sys
import os

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(project_dir))

class AudioUploadResourceTest(unittest.TestCase):
    def setUp(self):
        # Create a test Flask app instance and use it as the test client
        self.app = app.test_client()

    def test_upload_audio_success(self):
        # Specify the path to your actual audio file
        audio_file_path = '/Users/alcibar/Documents/BibleApp/casa_de_mi_padre/tests/S1 - enero 6 - Genesis 11.wav'

        # Check if the file exists
        self.assertTrue(os.path.isfile(audio_file_path), "Audio file does not exist")

        # Read the binary audio content from the specified file
        with open(audio_file_path, 'rb') as audio_file:
            audio_content = audio_file.read()

        # Ensure the file is not empty
        self.assertTrue(len(audio_content) > 0, "Audio file is empty")

        # Create a FileStorage object with the audio content
        audio_file = FileStorage(
            stream=io.BytesIO(audio_content),
            filename='test_audio.wav',  # Use the correct filename and content type for your audio file
            content_type='audio/wav'  # Replace with the correct content type if needed
        )

        # Validate the FileStorage object
        self.assertEqual(audio_file.filename, 'test_audio.wav')
        self.assertEqual(audio_file.content_type, 'audio/wav')

        # Make a POST request to the endpoint
        response = self.app.post('/upload-audio', data={'audio_file': audio_file})

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

    def test_upload_audio_missing_file(self):
        # Make a POST request without providing an audio file
        response = self.app.post('/upload-audio')

        # Check if the response status code is 400 (bad request)
        self.assertEqual(response.status_code, 400)

    def test_upload_audio_error(self):
        # Simulate an error scenario by causing an exception
        # You can customize this test case based on your error handling logic
        response = self.app.post('/upload-audio')

        # Check if the response status code is 500 (internal server error)
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()



