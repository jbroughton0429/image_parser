# Packer

This directory is meant for building out the 2 AMI images necessary for the AWS infrastructure. By default, both of these image use the following:

- AWS
- Default VPC {vpc_id}
- Default Subnet from the Default VPC {subnet_id}
- t2.micro Instance Type {instance_type}
- Ubuntu - Latest

### Variables
Both Images will require variables to be set prior to execution. These variables have been conviently located up at the top of the packer templates. The variables are as such:

- region: ((Region you are using))
- vpc_id: You can set this to anything in your environment, as it's just building an image. Default is best
- subnet_id: The subnet should be part of the vpc. Default is safe


# Specific Image Information

### Database Image
The database image is built off of MariaDB Server 10.3. Some of the key items that this server also automates is:

- Installs MariaDB
- Sets the Root Password for the database (Script for this is in ../scripts/reset_mysql_pw.sql)
- Creates an SSH Shared Key connection with the 'Console Server' - This allows the console server to establish a SSH Proxy Connection to the database.
- 
### Variables to Modify (Database)
Change the Password for MariaDB Root:
```sh
$ vim ../scripts/reset_msql_pw.sql
# Change Default Password in Line 9
```
Change Username and/or password for our default user:
```sh
$ vim ../scripts/build_db.sql
## Change Line Items 3 & 15 for the User if you wish to replace the user and/or password
```

### Console (DevOps) Image
The purpose of this image is to control the Database from a 'secure' location. In a normal environment, You wouldn't be making changes to a production database, from the database. However as this is also a test scenario (albeit can be expanded upon) the Console will be placed in the same VPC as the DataBase server. For this exercise, we will not only keep the machines separate, but allow the console server to control terraform.

- Installs All necessary Python3 Packages, and communcations to the mysql database
- Installs S3 Client for AWS, Terraform, Ansible and everything covered in your previous README on 'run_me_first.sh'
--This is done so that you can use the Console as a Terraform, Ansible, Packer, etc Devops/Jump station

# Building your Environment

1. Make sure that your AWS environment is setup first
    ```sh
    $ aws configure
    ```
2. Make your necessary changes (above) for Packer Variables. If this is the 2nd (or more) time you have run packer, you should modify the 'ami_name'. Increment this value as you continue building. (Ie: DevOps_1, DevOps_2)

3. Build Packer Image
    ```sh
    $ packer build packer_database-amazon.json
    $ packer build packer_devops-amazon.json
    ```
    *Note - You can run these two images simultaneously via GNU Screen*
4. When the images have completed building, they will output an AMI ID at the end. This ID is used automagically by Terraform to build your project

   
   
# Further Information

| Software | Website |
| ------ | ------ |
| Packer | [https://www.packer.io/][PlDb] |
| Terraform | [https://www.terraform.io/][PlGh] |
| MariaDB | [https://mariadb.org/][PlGd] |

