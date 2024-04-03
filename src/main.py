# # # main.py
# # import os
# # import pandas as pd
# # import gcsfs
# # import functions_framework
# # from google.cloud import pubsub_v1
# # from google.cloud import storage

# # @functions_framework.cloud_event
# # def gcs_to_pubsub(cloud_event):
# #      """Triggered by a file upload to a Cloud Storage bucket.
# #      Args:
# #           data (dict): Event payload.
# #           context (google.cloud.functions.Context): Metadata for the event.
# #      """
# #      data = cloud_event.data
# #      bucket_name = data['bucket']
# #      file_name = data['name']
# #      client = pubsub_v1.PublisherClient()
# #      # topic_path = client.topic_path(os.environ.get('PROJECT_ID'),
# #      #                               os.environ.get('TOPIC_NAME'))

# #      # # Read the file from GCS
# #      # storage_client = storage.Client(project=os.environ.get('PROJECT_ID'))
# #      # bucket = storage_client.bucket(bucket_name)
# #      # blob = bucket.blob(file_name)
# #      # file_content = blob.download_as_text()

# #      # print(blob.download_as_string())


# #      #     # Publish the file content to Pub/Sub
# #      #     data = file_content.encode("utf-8")
# #      #     future = client.publish(topic_path, data)
# #      #     print(future.result())

# #      # Replace 'your_bucket_name' and 'your_file_path.csv' with your actual bucket name and file path
# #      # bucket_url = 'gs://cloud-functions-trigger-bucket/customers-100.csv'

# #      # Read the CSV file from the GCS bucket into a pandas DataFrame
# #      # df = pd.read_csv(bucket_url)

# #      # Print the rows of the DataFrame
# #      # print(df)
# #      file_path = file_name
# #      fs = gcsfs.GCSFileSystem(project=os.environ.get('PROJECT_ID'))
# #      with fs.open(f'{bucket_name}/{file_path}') as f:
# #         df = pd.read_csv(f)
     
# #      print(df)
    
# # main.py
# import os
# import json
# import pandas as pd
# import gcsfs
# import functions_framework
# from google.cloud import pubsub_v1
# from google.cloud import storage


# @functions_framework.cloud_event
# def gcs_to_pubsub(cloud_event):
# #    data = cloud_event.data
# #    bucket_name = data['bucket']
# #    file_name = data['name']

# #    fs = gcsfs.GCSFileSystem(project=os.environ.get('PROJECT_ID'))
# #    with fs.open(f'{bucket_name}/{file_name}') as f:
# #       df = pd.read_csv(f)
   
# #    print(df.head())
#      publisher = pubsub_v1.PublisherClient()
#      topic_path = publisher.topic_path(os.environ.get('PROJECT_ID'),
#                                  os.environ.get('TOPIC_NAME'))
   
# #    for row_index, row in df.iterrows():
# #       message = json.dumps(row.to_dict()).encode('utf-8')
# #       future = publisher.publish(topic_path, data=message)
# #       print(future.result())

# #    print("DONE")
#      for n in range(1, 10):
#           data_str = f"Message number {n}"
#           # Data must be a bytestring
#           data = data_str.encode("utf-8")
#           # When you publish a message, the client returns a future.
#           future = publisher.publish(topic_path, data)
#           print(future.result())


import functions_framework
from google.cloud import pubsub_v1
import json
import pandas as pd
import gcsfs


# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def gcs_to_pubsub(cloud_event):
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket = data["bucket"]
    name = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("spartan-matter-417112", "cloud_function_trigger_topic")
    fs = gcsfs.GCSFileSystem(project="spartan-matter-417112")
    with fs.open(f'{bucket}/{name}') as f:
      df = pd.read_csv(f)

    df.reset_index(drop=True, inplace=True)

    for row_index, row in df.iterrows():
      message = json.dumps(row.to_dict()).encode('utf-8')
      future = publisher.publish(topic_path, data=message)
      print(future.result())
    print("Completed")