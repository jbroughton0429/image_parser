# image_parser
1. Execute the /scripts/run_me_first.sh to setup your dev environment - in Ubuntu 20.04
2. Change the necessary vars in ./packer/
packer_database-amazon.json  packer_devops-amazon.json
to match that of your AWS environment (Variables that are required are listed at the top)
3. Change your MySQL password: '/scripts/reset_mysql_pw.sql'
4. Build the two packer images
5. Edit TF Vars files: 
   - terraform/global/buckets/vars.tf (Add your Bucket information in)
   - terraform/devops/main.tf 
      = If you are in Prod Environment, switch Tags here to Prod from Dev
      = Change the AMI to that of the DevOps Image built from Packer (located in your AWS AMI Console)
   - terraform/platform/main.tf (ami - Same as devops, however the image for this one is labeled 'database')
      = If you are in Prod Environment, switch Tags here to Prod from Dev
      = Change the AMI to that of the DevOps Image built from Packer (located in your AWS AMI Console)
6. If this is your first time building TF in this environment, uncomment the 'bucket' line in:
   'deploy.sh'
7. Execute 'deploy.sh' to build the TF environment
8. Your 'Dev' Environment is no longer needed, log into 'Console' for all further steps.

## Console ##

To Log into the console, be sure to copy over your private keys from ./keys directory that was generated during the development phase. 
You will need this to login to both console and database servers.

1. The console is setup to make a ssh-key connection to the database server (passwordless). In order for the TDD script to initialize
correctly, run an SSH connection to validate this: ssh <ip-of-database-server> and accept the fingerprint.  After this you should no longer
need to accept fingerprint.

2. Tunnel.py is a reverse tunnel for the database server. Run this with ./tunnel.py -r <hostname-of-database-server> run it in the background to continue the connection. The default port is TCP/3337.


