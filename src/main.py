# main.py
import os
from google.cloud import pubsub_v1
from google.cloud import storage


def gcs_to_pubsub(data, context):
    """Triggered by a file upload to a Cloud Storage bucket.
    Args:
         data (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file = data
    bucket_name = file['bucket']
    file_name = file['name']
    client = pubsub_v1.PublisherClient()
    topic_path = client.topic_path(os.environ('PROJECT_ID'),
                                   os.environ('TOPIC_NAME'))

    # Read the file from GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    file_content = blob.download_as_text()

    # Publish the file content to Pub/Sub
    data = file_content.encode("utf-8")
    future = client.publish(topic_path, data)
    print(future.result())
