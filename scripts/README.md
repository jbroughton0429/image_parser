# Scripts (Bash and otherwise)

This is the automation scripts used to build out your environment. 

If you already have a free-standing environment with Python3 and MariaDB, the only information you will find useful here is **'build_db.sql'**

## Variables to modify
The SQL Files will be the only variables you modify in this directory
* build_db.sql - Line's 3 and 15 (Username and Password)
* reset_mysql_pw.sql - Line 9 - Root PW

## File Description

**build_db.sql** - This Script is generated *MANUALLY* on either the Database Server, or remotely from a secure connection, to: Build Database, setup tables, and create a user with permissions

**reset_mysql_pw.sql** - This Script is executed automagically via Packer to reset the DB Password. When installed without interaction, the database has some 'issues' with allowing root access remote until a password is locally set.

**run_me_first.sh** - This is executed by the Packer script to build out the Console/DevOps environment. It installs: Ansible, Terraform, Packer, putty-tools and the AWS CLI. These are necessary for building packer images, managing the terraform environment and loading keys via aws.

**_keygen.sh** - This builds out the keys for a few things: AWS private/public keypairs that are imported via TF, Public/private pairs that are imported via authorized_keys for sshkey comms between DevOps/Database, and generates putty keys for easy of communication.

**.screenrc** - Hidden! It's the screenrc that is moved over via packer, and very useful when you are building out several packer images and/or running the tunnel in 1 screen, sql connection in another (to check status) and the python script in a 3rd.

# Further Information

These scripts use the following tools:



| Software | Website |
| ------ | ------ |
| MariaDB | [https://www.mariadb.org][PlDb] |
| Puttygen | [https://www.puttygen.com][Plpu] |
| AWS CLI | [https://aws.amazon.com/cli/][Plaw] |




   [PlDb]: <https://www.mariadb.org>
   [Plpu]: <https://www.puttygen.com>
   [Plaw]: <https://aws.amazon.com/cli/>

