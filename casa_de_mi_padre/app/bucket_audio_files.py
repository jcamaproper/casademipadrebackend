from google.cloud import storage

def upload_audio_to_bucket(audio_file, project_id):
    # Create a storage client with explicit project ID
    storage_client = storage.Client(project=project_id)

    # Get the bucket
    bucket = storage_client.get_bucket("podcast_bucket_casa_de_mi_padre")

    # Upload the audio file
    blob = bucket.blob(audio_file.filename)
    blob.upload_from_string(audio_file.read(), content_type=audio_file.content_type)

    # Get the URL of the uploaded file
    file_url = blob.public_url

    return file_url