variable "project_id" {}
variable "zone" {
  default = "europe-southwest1-a"
}
variable "ssh_username" {
  default = "packer"
}

packer {
  required_plugins {
    googlecompute = {
      source  = "github.com/hashicorp/googlecompute"
      version = "~> 1"
    }
  }
}


source "googlecompute" "ubuntu_image" {
  project_id          = var.project_id
  source_image_family = "ubuntu-2204-lts"
  zone                = var.zone
  ssh_username        = var.ssh_username
  machine_type        = "e2-medium"
  image_name          = "central-vm-image"
}

build {
  sources = ["source.googlecompute.ubuntu_image"]

  provisioner "shell" {
    script = "files/install_prometheus_grafana_apache.sh"
  }
  provisioner "shell" {
    script = "files/custom_apt_repo.sh"
  }
}
