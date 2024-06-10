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
  image_name          = "student-vm-image"
}

build {
  sources = ["source.googlecompute.ubuntu_image"]

  provisioner "file" {
    source = "files/exam-validator.service"
    destination = "/tmp/exam-validator.service"
  }
  provisioner "file" {
    source = "files/requirements.txt"
    destination = "/tmp/requirements.txt"
  }
  provisioner "file" {
    source = "files/app.py"
    destination = "/tmp/app.py"
  }
  provisioner "shell" {
    script = "files/customize.sh"
  }
}
