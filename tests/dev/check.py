#!/usr/bin/python3
import subprocess
from subprocess import check_output

#s="aws s3 sync --dryrun s3://jaysons-legacy-image-bucket/image s3://jaysons-new-image-bucket/avatar"

proc = subprocess.run(['aws', 's3', 'sync', '--dryrun', 's3://jaysons-legacy-image-bucket/image', 's3://jaysons-new-image-bucket/avatar'], encoding='utf-8', stdout=subprocess.PIPE)
#for line in proc.stdout.split('\n'):

if 'dryrun' in proc.stdout:
    print(proc.stdout)
    print ("Migration Failed!")
    print ("Migration Failed!")
    print ("Migration Failed!")
else: 
    print ("Migration Successful!")

#print(stdout)
#if stdout.find("copy:") == -1: 
#    print ("Migration Successful!!")
#else:
#    print ("Migration Failed!")
#print (s)

#s = isinstance(line, str)
#print (s)
