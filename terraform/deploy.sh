#!/bin/bash
cd devops
terraform apply -auto-approve 
cd ../platform
terraform apply -auto-approve

# cd ../global/buckets/
#terraform destroy -auto-approve global/buckets/
