# Terraform

This directory is meant for building out the AWS Infrastructure for the 'Console', 'Database', and Buckets. This includes, but not limited to the following:

- AWS Backend - AWS Credentials are picked up from the AWS Pkg
- Buckets: Terraform State stored in bucket, 2x Buckets for project (Legacy, Modern)
- 2x VM's using the provided AMI's from Packer
- Security Groups built with only SSH access
- Machines:
--T2 Micro's with GP2, 30GB disks
-- Keys to access are generated from /scripts/keygen.sh, populated to /keys

### Variables
*This one needs Work - I've got to move my TF data into vars*

Buckets - [Bucket Data Path](/global/buckets/)
Inside of vars.tf you will need to modify lines: 4,10,16,22 for your respective environments

Line 4: Bucket Region
Line 10: Name of your TF State Bucket
Line 16: Name of your Legacy Bucket
Line 22: Name of your 'Production/Modern' Bucket

DevOps (Console) - [Console Data Path](/Devops/)
Inside of main.tf you will need to modify lines: 3, 8, 10, 48

Line 3: AWS Region
Line 8: TF State Bucket
Line 10: Bucket Region

Database - [Database Data Path](/platform/)
Database is aptly named 'platform' in case you wanted to add more servers/service to the production/platform environment, rather than just database. Database will require the same lines as DevOps: 3, 8, 10

Line 3: AWS Region
Line 8: TF State Bucket
Line 10: Bucket Region
Both Images will require variables to be set prior to execution. These variables have been conviently located up at the top of the packer templates. The variables are as such:

# Specific Image Information

### Database Image
The database image is built off of MariaDB Server 10.3. Some of the key items that this server also automates is:

As stated in the Packer Image README, the Database image is reachable via console(DevOps Machine) and SSH Tunnels. Keys are generated, and added to 'authorized_keys' when the image is build. The Server is locked down to SSH only. For testing purposes, SSH is externally exposed, but this can be removed once this becomes 'production ready'; as the console can connect to the Database Server.

There are two users for the Database server. Root and a 2nd user with limited privileges. This access is setup in the automation scripts, located in /scripts/ sub-directory

### Console (DevOps) Image
The purpose of this image is to control the Database from a 'secure' location. In a normal environment, You wouldn't be making changes to a production database, from the database. However as this is also a test scenario (albeit can be expanded upon) the Console will be placed in the same VPC as the Database server. For this exercise, we will not only keep the machines separate, but allow the console server to control terraform.

This Machine creates a tunnel to the Database server via a python package. Upon creation of the tunnel, all SQL traffic is passed through this tunnel.

The TF-State is stored in the bucket. This means that from this Console machine, we can manage the current state of the buckets and Database (production) environment. We 'could' in theory, modify the state of this running machine (firewall rules, network changes, etc) but it would be best to do this from your origional machine that build the packer images.

# Building your Environment

1. Make sure that your AWS environment is setup first
    ```sh
    $ aws configure
    ```
2. Make your necessary changes (above) for Terraform Variables. 
3. Modify the deploy.sh and destroy.sh files to add/remove the comment string if you are going to automate the creation of the bucket. *Note that Currently the bucket creation and destruction is commented out*
4. Execute deploy.sh
    ```sh
    $./deploy.sh
    ```
    This will build out your two environments (Database/Console), and if you uncommented the Buckets, build out your Buckets. 
    
**Please remember that you will need to uncomment the buckets for the first round, in order for TF-State to be built.**
5. Run the following commands to retrieve the Internal and External IP addresses of your instances (this will be used at a later state)
    ```sh
    $ terraform -chdir=devops show | grep public_ip
    $ terraform -chdir=platform show | grep private_ip
    ```
   
   
# Further Information

| Software | Website |
| ------ | ------ |
| Terraform | [https://www.terraform.io/][PlGh] |


