provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "terraform-state" {

  bucket = var.terraform-state
  acl    = "private"

  tags = {
    Name        = "TFState"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket" "legacy-bucket" {

  bucket = var.legacy-bucket
  acl = "private"

  tags = {
    Name = "legacybucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket" "new-bucket" {

bucket = var.new-bucket
  acl = "private"

  tags = {
    Name = "newbucket"
    Environment = "Dev"
  }
}

