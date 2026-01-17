variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "environment" {
  description = "Environment name (sandbox or production)"
  type        = string
}

variable "cloud_run_service_account_email" {
  description = "Cloud Run service account email for secret access"
  type        = string
}
