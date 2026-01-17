# VPC Network
resource "google_compute_network" "main" {
  name                    = "qr-payment-vpc-${var.environment}"
  auto_create_subnetworks = false
  project                 = var.project_id
}

# Subnet for Cloud Run VPC Connector
resource "google_compute_subnetwork" "main" {
  name          = "qr-payment-subnet-${var.environment}"
  ip_cidr_range = var.environment == "sandbox" ? "10.0.0.0/24" : "10.1.0.0/24"
  region        = var.region
  network       = google_compute_network.main.id
  project       = var.project_id

  private_ip_google_access = true
}

# Cloud Router for NAT
resource "google_compute_router" "main" {
  name    = "qr-payment-router-${var.environment}"
  region  = var.region
  network = google_compute_network.main.id
  project = var.project_id
}

# Static External IP for NAT (決済プロバイダIP制限用)
resource "google_compute_address" "nat" {
  name    = "qr-payment-nat-ip-${var.environment}"
  region  = var.region
  project = var.project_id
}

# Cloud NAT with Static IP
resource "google_compute_router_nat" "main" {
  name                               = "qr-payment-nat-${var.environment}"
  router                             = google_compute_router.main.name
  region                             = var.region
  project                            = var.project_id
  nat_ip_allocate_option             = "MANUAL_ONLY"
  nat_ips                            = [google_compute_address.nat.self_link]
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}

# VPC Access Connector for Cloud Run
# 名前は最大25文字: ^[a-z][-a-z0-9]{0,23}[a-z0-9]$
resource "google_vpc_access_connector" "main" {
  name          = "qr-pay-conn-${var.environment}"
  region        = var.region
  project       = var.project_id
  ip_cidr_range = var.environment == "sandbox" ? "10.8.0.0/28" : "10.9.0.0/28"
  network       = google_compute_network.main.name

  min_instances = 2
  max_instances = 3
}
