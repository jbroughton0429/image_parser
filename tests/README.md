# Migration Scripts (And Maintenance Scripts)
- [Migration Scripts (And Maintenance Scripts)](#migration-scripts--and-maintenance-scripts-)
  * [Variables to modify](#variables-to-modify)
- [Script Execution](#script-execution)
    + [Automation Script Environment](#automation-script-environment)
    + [Customer Provided Environment](#customer-provided-environment)
- [File Descriptions](#file-descriptions)
    + [Core](#core)
    + [Maintenance](#maintenance)
- [Further Information](#further-information)


This here is the 'meat and potatos' of the whole enterprise, the migration scripts. The core folder is aptly named 'tests', as we may be migrating the data to the new database, but we will not be deleting this data in the bucket, leaving us the ability to reverse the change (if necessary).

## Variables to modify
Each of the core scripts will have variables for modification. If you chose to use the 'maintenance' scripts (described below), they too will need Var modification

Variables are as follows:

**create-files\. py** 
- Lines 27/28 (Local Directories to create)
- Lines 32/33 (Bucket Names)
- Lines 44-48 (Database Information USER)

**move-files\. py** 
- Lines 26/27 (Bucket Names)
- Lines 30/31 (Bucket Directory Prefix)
- Lines 39-43 (Database Information USER)
- Line 79 - (Bucket Name/Location) ## Note: Jayson needs to turn this into vars##

_The below items are Maintenance Scripts and their Variables - They are not needed unless you are checking the status of the scripts/environment/maintenance_

**tunnel\. py** 
- Lines 27/28 (Remote/Local BIND Address for MariaDB)

**clean-up\. py**
- Lines 20/21 (Bucket Names)
- Line 27 (Local Directories created during 'create')
- Lines 32-37 (Database Information ROOT)

**ls-files\. py**
- Lines 13/14 (Bucket Names)

**sql-conn\. py**
- Lines 16-20 (Database Information ROOT)
- Line 30 (DB Info Table)

# Script Execution

There are two routes you can use if you are going to execute these scripts:
- From the Automation Script (TF/Packer built out everything for you)
- From your own Environment (No Automation Script)

We will cover both of these here, below is the full File descriptions for more information.

### Automation Script Environment
Here, most everything is controlled. You will need to make all necessary VAR changes to the following files:
- create-files
- move-files
- clean-up (In Maintenance folder)

If you want to run the maintenance scripts, make the necessary Var changes as well.

1. Start your screen session: $_screen_
2. Navigate to Screen 3 titled: <tunnel> and run the tunnel python script.
```sh 
$./tunnel.py -r <internalIPofDBServer>
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

### Customer Provided Environment
This assumes you already have a Database environment, your database can connect to the machine you are running this on, and all other necessities.

You will need to make all necessary VAR changes to the following files:
- /tests/move-files
- /scripts/build_db.sql (customer database username/password)
- Any maintenance files that you wish to use

1. Configure AWS CLI with your credentials (if you do not have this setup already)
```sh
$ aws configure
```
2. Cross your fingers and execute:
```sh
$./move-files.py
```
3. If successful you will be will receive 'Migration Successful' message. If failure, it will show you the files that failed to move over, with 'Migration Failed, 3x'
4. It is recommended, if you are using a _Customer Provided Environment_ to use the Functional Testing tools located in Maintenance, prior to executing the script, so that you can validate the Database connection, along with the bucket connection.

# File Descriptions

### Core
**create-files\. py** 
This script is used _ONLY_ if you do not have existing Avatars in separate buckets and the corresponding information in the database. The sole purpose of this script is for testing the _move-files\. py_ script without affecting a production-level environment.  With that, it does the following:
- Uses mktempfs to create _x_ and _y_ number of _legacy_ and _modern_ files, specified by the _-l_ and _-m_ command-line flag by the user. This will create the files onto the local filesystem, initially
- Upon creation, these files are then moved to the appropriate buckets and 'keys<folders>' in the buckets
- The information is reflected into a database with _'bucket'_ and _'filename'_

At this point you will have a devl environment similiar to that of the prod-like environment to do tests

**move-files\. py** 
This script does 3 main (or 4 depending on how you are counting) items:
- _Copy_ Data from legacy bucket to modern bucket
- Execute two SQL statements - in **buckets** Col replace 'legacy' with 'modern' / then swap 'image' with 'avatar' in the **file** Col
- Run _aws s3 sync --dryrun_ against the two buckets to verify that a copy was successful (Item #1), return success if successful, failure if failed.

**tunnel\. py**
If you are using the build script (TF/Packer, etc) this is an important part of the deployment. Tunnel creates and SSH tunnel to the Database server, and listens on port 3337 of your 'DevOps/Console' machine. When Packer built the image, it uses the public keys generated from the keygen script and placed this in the authorized_keys of the database server. It is necessary to start this tunnel up prior to running any of the other commands (create/move/cleanup)

### Maintenance

Maintenance is used for test/development tools. This is where the Functional Testing lives, along with cleaning up all the work to start fresh.

**clean-up\. py**
This resets everything.
- Deletes all of the local files created by the create-files script
- Deletes all files in buckets with the prefix of 'avatar'
- Truncates table 'avatars'

**ls-files\. py**
This script checks several items:
- Internet connection
- AWS Credentials from <aws configure> is addressed
- Buckets are created and populated
--Created via automation script TF, Populated from create-files script
- Post 'move-files', it is a quick way to verify that the copy was successful (Without needing to run sync)

**sql-conn\. py**
SQL Connection to check:
- Tunnel (if tunnel is used) is up and functioning
- Credentials are valid and database is created (From create_database sql)


# Further Information

These scripts use the following tools:



| Software | Website |
| ------ | ------ |
| SSHTunnel | [https://sshtunnel.readthedocs.io/en/latest/][Plst] |
| Argparse | [https://docs.python.org/3/library/argparse.html][Plap] |
| AWS CLI | [https://aws.amazon.com/cli/][Plaw] |
| Boto3 | [https://boto3.amazonaws.com/v1/documentation/api/latest/index.html][Plbo]|




   [Plst]: <https://sshtunnel.readthedocs.io/en/latest/>
   [Plap]: <https://docs.python.org/3/library/argparse.html>
   [Plaw]: <https://aws.amazon.com/cli/>
   [Plbo]: <https://boto3.amazonaws.com/v1/documentation/api/latest/index.html>

