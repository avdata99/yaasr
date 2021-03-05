import logging
import os
from google.cloud import storage


logger = logging.getLogger(__name__)
# Ensure load google credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "yaasr/settings/google-cloud-storage-credential.json"


def upload_to_google_cloud_storage(stream_path,
                                   metadata,
                                   bucket_name,
                                   destination_blob_name=None,
                                   delete_on_success=False):
    """Uploads a file to the Google Cloud storage bucket.
        Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
        """

    filename = stream_path.split('/')[-1]
    logging.info(f'Uploading {filename} to google cloud storage')
    if destination_blob_name is None:
        destination_blob_name = filename

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    # if bucket don't exists:
    # bucket = storage_client.create_bucket(bucket_name)

    blob = bucket.blob(destination_blob_name)
    if metadata is not None:
        blob.metadata = metadata
    blob.upload_from_filename(stream_path)

    logging.info(f'{filename} uploaded to google cloud storage at bucket {bucket_name} as {destination_blob_name}')

    if delete_on_success:
        logging.info(f'Deleting {stream_path}')
        os.remove(stream_path)

    return stream_path, metadata
