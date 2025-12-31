from google.cloud import storage
from urllib.parse import urlparse, unquote

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

# create a func to delete the file in the bucket
def delete_file_from_url(file_url, project_id, bucket_name):
    """
    Delete a file from Google Cloud Storage bucket given its URL.
    
    Args:
        file_url: The public URL of the file to delete
        project_id: The GCP project ID
        bucket_name: The name of the GCS bucket
    
    Returns:
        bool: True if the file was deleted, False if it didn't exist
    """
    # Create a storage client with explicit project ID
    storage_client = storage.Client(project=project_id)
    
    # Get the bucket
    bucket = storage_client.get_bucket(bucket_name)
    
    # Parse the URL to extract the blob name
    # URLs can be in format: https://storage.googleapis.com/{bucket}/{blob}
    # or: https://{bucket}.storage.googleapis.com/{blob}
    parsed_url = urlparse(file_url)
    blob_name = parsed_url.path.lstrip('/')
    
    # If the blob name starts with the bucket name, remove it
    if blob_name.startswith(bucket_name + '/'):
        blob_name = blob_name[len(bucket_name) + 1:]
    
    # URL-decode the blob name (e.g., %20 becomes space, %CC%81 becomes special chars)
    blob_name = unquote(blob_name)
    
    # Get the blob and delete it
    blob = bucket.blob(blob_name)
    
    if blob.exists():
        blob.delete()
        return True
    else:
        return False

        