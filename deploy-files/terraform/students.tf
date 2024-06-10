locals {
  students = jsondecode(file(var.json_file_path))
}

resource "google_compute_instance" "student_vm" {
  for_each = { for s in local.students : s.name => s }

  name         = each.value.name
  machine_type = "e2-small"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = var.student_image_name
    }
  }

  network_interface {
    network = "default"
    access_config {
    }
  }
  metadata = {
    ssh-keys = "${each.value.name}:${each.value.key}"
  }
}
