resource "google_cloudfunctions2_function" "function" {
  name        = "gcs-to-pubsub-function"
  location    = var.region
  description = "A function triggered by GCS to publish to Pub/Sub"

  build_config {
    runtime     = "python312"
    entry_point = "gcs_to_pubsub"
    environment_variables = {
      PROJECT_ID = var.project_id,
      TOPIC_NAME = google_pubsub_topic.topic.name

    }
    source {
      storage_source {
        bucket = google_storage_bucket.gcs-bucket-function.name
        object = google_storage_bucket_object.function_code.name
      }
    }
  }

  service_config {
    max_instance_count = 3
    min_instance_count = 0
    available_memory   = "256M"
    timeout_seconds    = 60

    ingress_settings               = "ALLOW_INTERNAL_ONLY"
    all_traffic_on_latest_revision = true
    service_account_email          = google_service_account.service_account.email
  }

  event_trigger {
    event_type            = "google.cloud.storage.object.v1.finalized"
    retry_policy          = "RETRY_POLICY_RETRY"
    service_account_email = google_service_account.service_account.email
    event_filters {
      attribute = "bucket"
      value     = google_storage_bucket.gcs-bucket-trigger.name
    }
  }

  depends_on = [google_service_account.service_account,
  google_project_iam_member.member-role]
}
