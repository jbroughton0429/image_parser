#!/bin/bash
cd devops
terraform init
terraform apply -auto-approve 
cd ../platform
terraform init
terraform apply -auto-approve

# cd ../global/buckets/
#terraform destroy -auto-approve global/buckets/
