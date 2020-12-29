#!/bin/bash

# Simple Bash script to Deploy Terraform Environment to AWS

# Init and Deploy Console Environment
cd devops
terraform init
terraform apply -auto-approve 

# Init and Deploy Production/Database Environment
cd ../platform
terraform init
terraform apply -auto-approve

<< ////
Uncomment this if this is the first time you are running
the Bucket creation. If buckets are already created, comment
this out.
////

# cd ../global/buckets/
# terraform init
#terraform destroy -auto-approve global/buckets/
