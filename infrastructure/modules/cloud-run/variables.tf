variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "asia-northeast1"
}

variable "environment" {
  description = "Environment name (sandbox or production)"
  type        = string
}

variable "service_account_email" {
  description = "Service account email for Cloud Run"
  type        = string
}

variable "vpc_connector_id" {
  description = "VPC Access Connector ID"
  type        = string
}

variable "image" {
  description = "Container image URL"
  type        = string
  default     = ""
}

# Secret Manager secret IDs
variable "paypay_api_key_secret_id" {
  description = "PayPay API Key secret ID"
  type        = string
  default     = ""
}

variable "paypay_api_secret_secret_id" {
  description = "PayPay API Secret secret ID"
  type        = string
  default     = ""
}

variable "paypay_merchant_id_secret_id" {
  description = "PayPay Merchant ID secret ID"
  type        = string
  default     = ""
}
