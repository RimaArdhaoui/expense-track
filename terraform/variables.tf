variable "kubeconfig_path" {
  type = string
}

variable "image_name" {
  type = string
}

variable "app_secret_key" {
  type      = string
  sensitive = true
}