from google.cloud import storage

def upload_file_to_bucket(file, project_id, bucket_name):
    # Create a storage client with explicit project ID
    storage_client = storage.Client(project=project_id)

    # Get the bucket
    bucket = storage_client.get_bucket(bucket_name)

    # Upload the file
    blob = bucket.blob(file.filename)
    blob.upload_from_string(file.read(), content_type=file.content_type)

    # Make the blob publicly accessible
    blob.make_public()

    # Get the URL of the uploaded file
    file_url = blob.public_url

    return file_url

# Create a func to check if the file already exists in the bucket
def check_file_exists(file, project_id, bucket_name):
    # Create a storage client with explicit project ID
    storage_client = storage.Client(project=project_id)

    # Get the bucket
    bucket = storage_client.get_bucket(bucket_name)

    # Check if the file exists
    blob = bucket.blob(file.filename)
    return blob.exists()