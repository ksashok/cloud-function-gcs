resource "google_storage_bucket" "gcs-bucket" {
  name     = "cloud-functions-terraform-bucket"
  location = var.region
}

resource "google_storage_bucket_object" "function_code" {
  name   = "function.zip"
  bucket = google_storage_bucket.gcs-bucket.name
  source = data.archive_file.function_code.output_path
}