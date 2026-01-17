terraform {
  backend "gcs" {
    bucket = "tadakayo-qr-connect-tfstate"
    prefix = "terraform/sandbox"
  }
}
