variable "google_credential" {
  description = "gcp service account credential"
  default = "/home/vice/DEZ/week1/terraform-demo/key/dez-jimmyh-8562b53534c1.json"
}

variable "project" {
  description = "project name"
  default = "dez-jimmyh"
}

variable "region" {
  description = "GCP region"
  default = "australia-southeast1"
}

variable "google_storage_bucket" {
  description = "GCP bucket name"
  default = "dez-w1-bucket"
}



variable "bq_dataset_id" {
  description = "bigquery dataset id"
  default = "w1_dataset"
}