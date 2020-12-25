#!/bin/bash
cd devops/
terraform destroy -auto-approve 
cd ../platform
terraform destroy -auto-approve 
#cd ../global/buckets
#terraform destroy -auto-approve global/buckets/
