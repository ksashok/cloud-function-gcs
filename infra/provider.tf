terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.21.0"
    }
  }
}

provider "google" {
  project = "spartan-matter-417112"
  region  = "australia-southeast1"
}