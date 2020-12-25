variable "region" {
  description = "Region"
  type = string
  default = "us-east-1"
  }

variable "terraform-state" {
  description = "Name of the TFState Bucket"
  type = string
  default = "jaysons-fancy-terraform-state"
  }

variable "legacy-bucket" {
  description = "Name of the Legacy image bucket"
  type = string
  default = "jaysons-legacy-image-bucket"
  }

variable "new-bucket" {
  description = "Name of the new image bucket"
  type = string
  default = "jaysons-new-image-bucket"
  }

