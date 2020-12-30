Vars:
Packer-Files (/packer)
* In variables area: modify region, vpc_id and subnet_id for your environment

SQL Code - (/scripts)
build_db.sql - change rtrenneman's default password (line 3)
reset_mysql_pw.sql - change root default password

Terraform - (/terraform)

deploy.sh - Uncomment the bucket item if this is the first time building your bucket.

global/bucket/vars.tf - Change the region, and name of your 3 buckets (tfstate, legacy and production)

///AFTER Packer Built/// devops/main.tf & platform/main.tf respectivly - Change the AMI ID under to reflect that of the
	created AMI from packer

1. Execute: /scripts/run_me_first.sh 
2. Run: <aws configure> to setup keys for terraform
3. Execute: /scripts/keygen.sh ((Time to complete 1-3 - 5min))
4. cd packer && packer build packer_database-amazon.json - Upon completion, copy the AMI-ID at the end of the script, place it
   into the terraform: /terraform/platform/main.tf
5. Do the same for the devops/console machine: packer build packer_devops-amazon.json. Upon completion, copy the AMI-ID to:
   /terraform/devops/main.tf ((Time to complete 4/5 - 10min))
6. Run terraform build script:
	cd /terraform
	./build.sh
7. Run the following commands to get Internal IP addresses of your instances (copy both for later):
	terraform -chdir=devops show | grep public_ip
	terraform -chdir=platform show | grep private_ip
	((Time to complete - 1 minute))
	
	

**Copy out your keys from <keys> directory - This Console is no longer needed and can be shut down (you can use it to destroy the environment when we are completed)**
1. SSH to Console/Devops
2. Run: screen
3. switch to 'tunnel' and start up the tunnel to the database
	a. cd tests && ./tunnel.py -r <ipaddr-db-svr>
	b. An established tunnel will result in TCP:/3337
4. switch to 'console-svr' 
5. run: aws configure, to setup AWS in the console environment
6. Build the Database: (automate this in packer)
	a. cd scripts/
	a. mysql -h "127.0.0.1" -P 3337 -u "root" -p "mysql" < "build_db.sql"
7. Edit: /tests/create-files.py and specify your 'legacy_bucket' and 'modern_bucket' locations.
8. Run ./create-files.py -l <# of legacy avatar images to create> -m <# of modern avatar images to create>
	((Total time - 5min))
9. 
