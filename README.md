# S3 Move Files / Update Records

- [S3 Move Files / Update Records](#s3-move-files---update-records)
  * [Customer Provided Environment](#customer-provided-environment)
  * [Automation Script Environment](#automation-script-environment)
    + [Setup Variables](#setup-variables)
    + [Pre-Build (Build out Infra)](#pre-build--build-out-infra-)
    + [Post-Build (Run Move Scripts)](#post-build--run-move-scripts-)

This README is a multi-part readme that can be broken down and read in any section that the reader feels necessary for their deployment scenarios. If you already have a SQL and Python environment, you can skip to <>. If you will be building/automating your own environment, than skip to <>
- /packer - README covers the image building process
- /terrraform - README covers Terraform Automation and deployment for AWS (Creating 2 images)
- /scripts - README covers each individual script and their grand purpose in the 2 deployment scenarios
- /tests README is the _creme de la creme_, this is what you are here for. It covers each script, and the 2 deployment scenarios in depth.

## Customer Provided Environment
Use this scenario if you already have your own environment (Python/SQL) and want to just execute the code.

_This assumes you already have a Database environment, your database can connect to the machine you are running this on, and all other necessities_

You will need to make all necessary VAR changes to the following files:
- /tests/move-files
- /scripts/build_db.sql (customer database username/password)
- Any maintenance files that you wish to use (Located in: tests/maintenance).
--Further information on each test file and the Maintenance file can be found in _/test/README.md_

1. Configure AWS CLI with your credentials (if you do not have this setup already)
```sh
$ aws configure
```
2. Cross your fingers and execute:
```sh
$./move-files.py
```
3. If successful you will be will receive 'Migration Successful' message. If failure, it will show you the files that failed to move over, with 'Migration Failed, 3x'
4. It is recommended, if you are using a _Customer Provided Environment_ to use the Functional Testing tools located in Maintenance, prior to executing the script, so t
hat you can validate the Database connection, along with the bucket connection.

## Automation Script Environment

Automation/Build is much more indepth; albeit it does build out a full environment for testing scenarios. You will be given a MariaDB server, and a 'DevOps/Console' server that makes an SSH tunnel back to the MariaDB environment for secure connections.

_Note: You will do your initial deployment on an Ubuntu:Latest machine (feel free to change run_me_first.sh to meet your platform of preference. This will allow you to deploy and destroy your TF environments_

### Setup Variables

**Packer-Files (/packer)**
* In variables area: modify region, vpc_id and subnet_id for your environment

**SQL Code - (/scripts)**
* build_db.sql - change rtrenneman's default password (line 3) (_or create your own user_)
* reset_mysql_pw.sql - change root default password

**Terraform - (/terraform)**
* deploy .sh - Uncomment the bucket item if this is the first time building your bucket.
*global/bucket/vars.tf - Change the region, and name of your 3 buckets (tfstate, legacy and production)
*devops/main.tf & platform/main.tf - Change the region and your bucket name of your tfstate.

**Tests - (/tests)**
- /tests/create-files.py
--Lines 32/33 - Bucket Names of Legacy and Modern
--Lines 44-45 - Database ROOT - Login/Password (_if changed_)
- /tests/move-files.py
--Lines 26/27 - Bucket Names of Legacy and Modern
--Lines 39/40 - Database USER - Login/Password (_if changed_)
- /tests/maintenance/clean-up.py (In Maintenance folder)
--Lines 24/25 - Bucket Names for Legacy and Modern
-- Lines 33/34 - Database ROOT - Login/Password (_if changed_)
If you want to run the maintenance scripts, make the necessary Var changes as well.

## Pre-Build (Build out Infra)
1. Build your environment:
```sh
$ cd scripts
$ ./run_me_first.sh
```
2. Generate SSH keys needed for AWS and authorized_keys communication between servers
```sh
~/image_parser/scripts$ ./keygen.sh
```
3. Setup AWS Credentials
```sh
$ aws configure
```
4. Build your packer images
```sh
$ cd packer
~/image_parser/packer$ packer build packer_database-amazon.json
## After image has been built (or in a screen session), build DevOps Image
~/image_parser/packer$ packer build  packer_devops-amazon.json
```
5. After both images have been built, start the Terraform and pull your IP Addresses
```sh
$ cd terraform/
# If this is the first time running build.sh, uncomment the Bucket build in the script.
~/image_parser/terraform$ ./deploy.sh
# After success, fetch IP Addresses of machines
~/image_parser/terraform$ terraform -chdir=devops show | grep public_ip
~/image_parser/terraform$ terraform -chdir=platform show | grep private_ip
```
6. Copy out your keys (ppk for putty is generated) from the /keys directory. This server can be shut down until necessary to Terraform-Destroy (To destroy, run ./destroy.sh inside of terraform script)

### Post-Build (Run Move Scripts)

_Note: These steps are issued from the DevOps/Console Machine that you built from TF. The IP Address was gathered in step 5 'public_ip'._ 
1. Start your screen session: _screen_
2. Navigate to Screen 3 titled: <tunnel> and run the tunnel python script.
```sh
$./tunnel.py -r <internalIPofDBServer>
# Fetched from Step 5 above (private_ip)
```
3. Switch to Screen 1<console-svr>.
- Navigate to scripts and edit _build\_db.sql_ to reflect your Local Username/Password
- Execute the following:
```sh
$ mysql -h "127.0.0.1" -P 3337 -u "root" -p "mysql" < "build_db.sql"
# Enter your root MySQL Password when prompted
```
4. Setup your AWS Credentials
```sh
$ aws configure
```
5. You can use Screen 2<database-svr> to establish a tunneled DB connection, checking the progress via:
```sh
$ mysql -h "127.0.0.1" -P 3337 -u "<yourusername>" -p "avatar_db"
```
6. In screen 1<console-svr> Execute the following commands:
```sh
$ cd tests
$ ./create-files.py -l <num-legacy-create> -m <num-modern-create>
# If you have 'ls-files.py' in maintenance, or a DB conn open, you
# can see these files in AWS and the database
./move-files.py
```
7. Once you have verified everything is completed, it's time to delete/reset the environment:
```sh
$ cd tests/maintenance
$ clean-up.py
```

From the machine that you initially created DevOps/Database, you can destroy your AWS Environment (Machines/Buckets):
```sh
~/image_parser$ cd terraform/
# Comment out bucket info in destroy.sh if you want to destroy bucket
~/image_parser/terraform$ ./destroy.sh
```



| Software | Website |
| ------ | ------ |
| Terraform | [https://terraform.io][PlTe] |
| Packer | [https://www.packer.io/][PlPa] |
| MariaDB | [http://mariadb.org/][PlMa] |
| Ansible | [https://www.ansible.com/][PlAn] |
| AWS CLI | [https://aws.amazon.com/cli/][PlAw] |
| Python 3 | [https://www.python.org/download/releases/3.0/][PlPy] |




   [PlTe]: <https://terraform.io>
   [PlPa]: <https://www.packer.io/>
   [PlMa]: <http://mariadb.org/>
   [PlAn]: <https://www.ansible.com/>
   [PlAw]: <https://aws.amazon.com/cli/>
   [PlPy]: <https://www.python.org/download/releases/3.0/>

