# Secret Manager secrets for payment provider credentials
# Note: Secret values are set manually via Console or gcloud CLI

locals {
  env_suffix = upper(var.environment)
}

# PayPay API Key
resource "google_secret_manager_secret" "paypay_api_key" {
  secret_id = "PAYPAY_API_KEY_${local.env_suffix}"
  project   = var.project_id

  replication {
    auto {}
  }
}

# PayPay API Secret
resource "google_secret_manager_secret" "paypay_api_secret" {
  secret_id = "PAYPAY_API_SECRET_${local.env_suffix}"
  project   = var.project_id

  replication {
    auto {}
  }
}

# PayPay Merchant ID
resource "google_secret_manager_secret" "paypay_merchant_id" {
  secret_id = "PAYPAY_MERCHANT_ID_${local.env_suffix}"
  project   = var.project_id

  replication {
    auto {}
  }
}

# Rakuten Pay API Key
resource "google_secret_manager_secret" "rakuten_api_key" {
  secret_id = "RAKUTEN_API_KEY_${local.env_suffix}"
  project   = var.project_id

  replication {
    auto {}
  }
}

# Rakuten Pay API Secret
resource "google_secret_manager_secret" "rakuten_api_secret" {
  secret_id = "RAKUTEN_API_SECRET_${local.env_suffix}"
  project   = var.project_id

  replication {
    auto {}
  }
}

# Grant Cloud Run SA access to all secrets
resource "google_secret_manager_secret_iam_member" "paypay_api_key" {
  secret_id = google_secret_manager_secret.paypay_api_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${var.cloud_run_service_account_email}"
}

resource "google_secret_manager_secret_iam_member" "paypay_api_secret" {
  secret_id = google_secret_manager_secret.paypay_api_secret.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${var.cloud_run_service_account_email}"
}

resource "google_secret_manager_secret_iam_member" "paypay_merchant_id" {
  secret_id = google_secret_manager_secret.paypay_merchant_id.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${var.cloud_run_service_account_email}"
}

resource "google_secret_manager_secret_iam_member" "rakuten_api_key" {
  secret_id = google_secret_manager_secret.rakuten_api_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${var.cloud_run_service_account_email}"
}

resource "google_secret_manager_secret_iam_member" "rakuten_api_secret" {
  secret_id = google_secret_manager_secret.rakuten_api_secret.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${var.cloud_run_service_account_email}"
}
