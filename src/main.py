import functions_framework
import os
from google.cloud import pubsub_v1
import json
import pandas as pd
import gcsfs


# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def gcs_to_pubsub(cloud_event):
     data = cloud_event.data
     bucket = data["bucket"]
     name = data["name"]

     fs = gcsfs.GCSFileSystem(project=os.environ.get('PROJECT_ID'))
     with fs.open(f'{bucket}/{name}') as f:
          df = pd.read_csv(f)

     publisher = pubsub_v1.PublisherClient()
     topic_path = publisher.topic_path(os.environ.get('PROJECT_ID'),
                                   os.environ.get('TOPIC_NAME'))

     for row_index, row in df.iterrows():
          message = json.dumps(row.to_dict()).encode('utf-8')
          future = publisher.publish(topic_path, data=message)
          print(future.result())
     print("Completed")