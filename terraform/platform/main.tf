provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "jaysons-fancy-terraform-state"
    key    = "production/tfstate/key"
    region = "us-east-1"
  }
}

resource "aws_key_pair" "database" {
  key_name   = "production"
  public_key = file("../../keys/database.pub")
}

resource "aws_security_group" "database" {
  name        = "Database Servers"
  description = "Allow SSH"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "database"
    Env = "Dev"
    Sol = "terraform"
  }
}

data "aws_ami" "database" {
  owners = ["self"]
  most_recent = true

  filter {
    name = "state"
    values = ["available"]
  }
  filter {
    name = "tag:Name"
    values = ["Database"]
 }
}


resource "aws_instance" "database" {
  key_name      = aws_key_pair.database.key_name
  ami           = data.aws_ami.database.id
  instance_type = "t2.micro"

  tags = {
    Name = "database"
    Env = "Dev"
    Sol = "terraform"
  }

  vpc_security_group_ids = [
    aws_security_group.database.id
  ]

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("key")
    host        = self.public_ip
  }

  ebs_block_device {
    device_name = "/dev/sda1"
    volume_type = "gp2"
    volume_size = 30
  }
}

resource "aws_eip" "database" {
  vpc      = true
  instance = aws_instance.database.id
}

