#!/bin/bash


sudo apt update
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt-get update --yes
sudo apt install --yes software-properties-common ansible terraform packer

