resource "google_service_account" "service_account" {
  project      = var.project_id
  account_id   = "cloud-function-worker"
  display_name = "Cloud Function Service Account"
}

resource "google_project_iam_custom_role" "cfunction_role" {
  role_id     = "customCFunctionRole"
  title       = "Custom Cloud Function Role"
  description = "Permissions for Cloud Function to interact with GCS and BigQuery"
  permissions = [
    "storage.objects.get",
    "eventarc.events.receiveEvent",
    "eventarc.events.receiveAuditLogWritten",
    "run.executions.cancel",
    "run.jobs.run",
    "run.routes.invoke"
  ]
}

resource "google_project_iam_binding" "service_account_binding" {
  project = var.project_id
  role    = google_project_iam_custom_role.cfunction_role.id

  members = [
    "serviceAccount:${google_service_account.service_account.email}",
  ]
}
