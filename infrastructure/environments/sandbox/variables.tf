variable "project_id" {
  description = "GCP Project ID"
  type        = string
  default     = "tadakayo-qr-connect"
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "asia-northeast1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "sandbox"
}

variable "github_repo" {
  description = "GitHub repository in format 'owner/repo'"
  type        = string
  default     = "yasushi-honda-prog/tadakayo-qr-charity-connect"
}
