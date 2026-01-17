output "paypay_api_key_secret_id" {
  description = "PayPay API Key secret ID"
  value       = google_secret_manager_secret.paypay_api_key.secret_id
}

output "paypay_api_secret_secret_id" {
  description = "PayPay API Secret secret ID"
  value       = google_secret_manager_secret.paypay_api_secret.secret_id
}

output "paypay_merchant_id_secret_id" {
  description = "PayPay Merchant ID secret ID"
  value       = google_secret_manager_secret.paypay_merchant_id.secret_id
}

output "rakuten_api_key_secret_id" {
  description = "Rakuten Pay API Key secret ID"
  value       = google_secret_manager_secret.rakuten_api_key.secret_id
}

output "rakuten_api_secret_secret_id" {
  description = "Rakuten Pay API Secret secret ID"
  value       = google_secret_manager_secret.rakuten_api_secret.secret_id
}
