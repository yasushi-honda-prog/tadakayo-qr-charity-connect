terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# IAMモジュール
module "iam" {
  source = "../../modules/iam"

  project_id  = var.project_id
  region      = var.region
  environment = var.environment
  github_repo = var.github_repo
}

# ネットワークモジュール
module "networking" {
  source = "../../modules/networking"

  project_id  = var.project_id
  region      = var.region
  environment = var.environment
}

# Firestoreモジュール
module "firestore" {
  source = "../../modules/firestore"

  project_id = var.project_id
  region     = var.region
}

# Secretsモジュール
module "secrets" {
  source = "../../modules/secrets"

  project_id                      = var.project_id
  environment                     = var.environment
  cloud_run_service_account_email = module.iam.cloud_run_service_account_email
}

# Cloud Runモジュール
module "cloud_run" {
  source = "../../modules/cloud-run"

  project_id            = var.project_id
  region                = var.region
  environment           = var.environment
  service_account_email = module.iam.cloud_run_service_account_email
  vpc_connector_id      = module.networking.vpc_connector_id

  # Secret Manager secrets
  paypay_api_key_secret_id     = module.secrets.paypay_api_key_secret_id
  paypay_api_secret_secret_id  = module.secrets.paypay_api_secret_secret_id
  paypay_merchant_id_secret_id = module.secrets.paypay_merchant_id_secret_id
}

# 出力
output "cloud_run_service_account_email" {
  value = module.iam.cloud_run_service_account_email
}

output "github_actions_service_account_email" {
  value = module.iam.github_actions_service_account_email
}

output "workload_identity_provider" {
  value = module.iam.workload_identity_provider
}

output "nat_ip" {
  description = "Static NAT IP (for payment provider whitelist)"
  value       = module.networking.nat_ip
}

output "vpc_connector_name" {
  value = module.networking.vpc_connector_name
}

output "cloud_run_service_url" {
  description = "Cloud Run service URL"
  value       = module.cloud_run.service_url
}
