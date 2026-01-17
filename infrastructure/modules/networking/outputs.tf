output "vpc_id" {
  description = "VPC Network ID"
  value       = google_compute_network.main.id
}

output "vpc_name" {
  description = "VPC Network Name"
  value       = google_compute_network.main.name
}

output "subnet_id" {
  description = "Subnet ID"
  value       = google_compute_subnetwork.main.id
}

output "nat_ip" {
  description = "Static NAT IP address (for payment provider whitelist)"
  value       = google_compute_address.nat.address
}

output "vpc_connector_id" {
  description = "VPC Access Connector ID for Cloud Run"
  value       = google_vpc_access_connector.main.id
}

output "vpc_connector_name" {
  description = "VPC Access Connector Name"
  value       = google_vpc_access_connector.main.name
}
