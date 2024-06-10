resource "google_service_account" "central_sa" {
  account_id   = "central-sa"
  display_name = "Central VM Service Account"
}

resource "google_project_iam_member" "central_sa_role" {
  project = var.project_id
  role    = "roles/compute.viewer"
  member  = "serviceAccount:${google_service_account.central_sa.email}"
}

resource "google_compute_instance" "central_vm" {
  name         = "central-vm"
  machine_type = "e2-medium"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = var.central_image_name
    }
  }

  network_interface {
    network = "default"
    access_config {
    }
  }
  service_account {
    email  = google_service_account.central_sa.email
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }
  metadata = {
    ssh-keys = "${var.teacher_name}:${var.teacher_ssh_key}"
  }
}