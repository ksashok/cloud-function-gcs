resource "google_cloudfunctions_function" "function" {
 name                 = "gcs-to-pubsub-function"
 description           = "A function triggered by GCS to publish to Pub/Sub"
 runtime               = "python312"
 available_memory_mb   = 256
 source_archive_bucket = google_storage_bucket.gcs-bucket-function.name
 source_archive_object = google_storage_bucket_object.function_code.name
 trigger_event         = "google.storage.object.finalize"
 trigger_resource      = google_storage_bucket.gcs-bucket-trigger.name
 entry_point           = "gcs_to_pubsub"
 service_account_email = google_service_account.service_account.email
}
