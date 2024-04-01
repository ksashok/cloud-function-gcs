resource "google_storage_bucket" "gcs-bucket-function" {
  name     = "cloud-functions-code-bucket"
  location = var.region
}

resource "google_storage_bucket" "gcs-bucket-trigger" {
  name     = "cloud-functions-trigger-bucket"
  location = var.region
}

resource "google_storage_bucket_object" "function_code" {
  name   = "function.zip"
  bucket = google_storage_bucket.gcs-bucket-function.name
  source = data.archive_file.function_code.output_path
}