resource "google_pubsub_topic" "topic" {
  name    = "cloud_function_trigger_topic"
  project = var.project_id
}
