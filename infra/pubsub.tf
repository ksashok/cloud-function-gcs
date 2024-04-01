resource "google_pubsub_topic" "topic" {
 name = "cloud_function_trigger_topic"
 project = var.project_id
}

resource "google_pubsub_topic_iam_binding" "binding" {
  project = google_pubsub_topic.topic.project
  topic = google_pubsub_topic.topic.name
  role = "roles/pubsub.publisher"
  members = [
    "serviceAccount:${google_service_account.service_account.email}",
 ]
}
