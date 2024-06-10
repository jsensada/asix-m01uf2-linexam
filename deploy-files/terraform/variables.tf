variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The region where the exam resources will be deployed"
  type        = string
  default     = "europe-southwest1"
}

variable "zone" {
  description = "The zone within the region where the exam resources will be deployed"
  type        = string
  default     = "europe-southwest1-a"
}

variable "json_file_path" {
  description = "Path to the JSON file containing the students data"
  type        = string
}

variable "student_image_name" {
  description = "Name of the packer image to deploy for each student"
  type        = string
  default     = "student-vm-image"
}

variable "central_image_name" {
  description = "Name of the packer image to deploy as central vm"
  type        = string
  default     = "central-vm-image"
}

variable "teacher_ssh_key" {
  description = "Teacher SSH_KEY to access to cetnral-vm"
  type        = string
}

variable "teacher_name" {
  description = "Teacher usernmaname to access to cetnral-vm"
  type        = string
  default     = "jsensada"
}