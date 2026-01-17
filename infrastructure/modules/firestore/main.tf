# Firestore Database (Native mode)
resource "google_firestore_database" "main" {
  project     = var.project_id
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"

  # Prevent accidental deletion
  deletion_policy = "DELETE"
}

# Firestore Index for donations collection
# status + createdAt (for listing donations by status)
resource "google_firestore_index" "donations_status_created" {
  project    = var.project_id
  database   = google_firestore_database.main.name
  collection = "donations"

  fields {
    field_path = "status"
    order      = "ASCENDING"
  }

  fields {
    field_path = "createdAt"
    order      = "DESCENDING"
  }
}

# provider + providerOrderId (for looking up by payment provider)
resource "google_firestore_index" "donations_provider_order" {
  project    = var.project_id
  database   = google_firestore_database.main.name
  collection = "donations"

  fields {
    field_path = "provider"
    order      = "ASCENDING"
  }

  fields {
    field_path = "providerOrderId"
    order      = "ASCENDING"
  }
}

# source + createdAt (for analytics by QR source)
resource "google_firestore_index" "donations_source_created" {
  project    = var.project_id
  database   = google_firestore_database.main.name
  collection = "donations"

  fields {
    field_path = "source"
    order      = "ASCENDING"
  }

  fields {
    field_path = "createdAt"
    order      = "DESCENDING"
  }
}
