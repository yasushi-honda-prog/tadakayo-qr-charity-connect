locals {
  service_name = var.environment == "production" ? "qr-payment-api" : "qr-payment-api-sandbox"
  # Use placeholder image for initial deployment if no image specified
  container_image = var.image != "" ? var.image : "gcr.io/cloudrun/hello"
}

# Cloud Run Service
resource "google_cloud_run_v2_service" "api" {
  name     = local.service_name
  location = var.region
  project  = var.project_id

  template {
    service_account = var.service_account_email

    # Use VPC connector for egress (fixed IP via Cloud NAT)
    vpc_access {
      connector = var.vpc_connector_id
      egress    = "ALL_TRAFFIC"
    }

    containers {
      image = local.container_image

      ports {
        container_port = 8080
      }

      env {
        name  = "ENVIRONMENT"
        value = var.environment
      }

      env {
        name  = "PROJECT_ID"
        value = var.project_id
      }

      env {
        name  = "REGION"
        value = var.region
      }

      # PayPay credentials from Secret Manager
      dynamic "env" {
        for_each = var.paypay_api_key_secret_id != "" ? [1] : []
        content {
          name = "PAYPAY_API_KEY"
          value_source {
            secret_key_ref {
              secret  = var.paypay_api_key_secret_id
              version = "latest"
            }
          }
        }
      }

      dynamic "env" {
        for_each = var.paypay_api_secret_secret_id != "" ? [1] : []
        content {
          name = "PAYPAY_API_SECRET"
          value_source {
            secret_key_ref {
              secret  = var.paypay_api_secret_secret_id
              version = "latest"
            }
          }
        }
      }

      dynamic "env" {
        for_each = var.paypay_merchant_id_secret_id != "" ? [1] : []
        content {
          name = "PAYPAY_MERCHANT_ID"
          value_source {
            secret_key_ref {
              secret  = var.paypay_merchant_id_secret_id
              version = "latest"
            }
          }
        }
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }

      startup_probe {
        http_get {
          path = "/health"
        }
        initial_delay_seconds = 0
        timeout_seconds       = 3
        period_seconds        = 10
        failure_threshold     = 3
      }

      liveness_probe {
        http_get {
          path = "/health"
        }
        timeout_seconds   = 3
        period_seconds    = 30
        failure_threshold = 3
      }
    }

    scaling {
      min_instance_count = 0
      max_instance_count = 10
    }

    timeout = "60s"
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

# Allow unauthenticated access (public API)
resource "google_cloud_run_v2_service_iam_member" "public" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.api.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
