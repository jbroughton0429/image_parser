#!/usr/bin/env python3

# 
# Core Script: Move/Migate Data
#
# This script will COPY data from the 'legacy' bucket to the 'modern' bucket (note: Copy, not delete)
# After copy, the script executes SQL to change the 'URL' to that of the modern URL, along with the filepath to
# Match the new URL.  
#
# Validation happens with 'checkdata()', running aws s3 sync to validate that the data was copied to the modern
# Bucket
#
# Shamelessly plucked the bucket-to-bucket migration from:
# https://stackoverflow.com/questions/43458001/can-we-copy-the-files-and-folders-recursively-between-aws-s3-buckets-using-boto3

import boto3
import mariadb
import subprocess

## Vars for Buckets and 'folder' prefixes
# Declaring S3 WAY early as I need it a few lines down for old/new bucket
s3 = boto3.resource('s3')


bucket = {
        "legacy": "jaysons-legacy-image-bucket", 
        "modern": "jaysons-new-image-bucket"
        }
prefix = {
        "legacy": 'image',
        "modern": 'avatar'
        }
old_bucket = s3.Bucket(bucket["legacy"])
new_bucket = s3.Bucket(bucket["modern"])

# MariaDB Connector

try: conn = mariadb.connect(
		user="rtrenneman",
		password="haveyouturneditoffandonagain",
		host="127.0.0.1",
		port=3337,
		database="avatar_db"
	)
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Twofer - Migrate data from Legacy bucket to the new bucket, then update the 
# Database with changes to the bucket path, and folder path

def migratedata():
    
    cursor = conn.cursor()

    for obj in old_bucket.objects.filter(Prefix=prefix["legacy"]):
        old_source = { 'Bucket': bucket["legacy"],
                    'Key': obj.key}
        new_key = obj.key.replace(prefix["legacy"], prefix["modern"], 1)
        new_obj = new_bucket.Object(new_key)
        new_obj.copy(old_source)

    try: 
        cursor.execute("UPDATE avatars SET bucket = replace(bucket,%s,%s)",(bucket["legacy"],bucket["modern"]))
        cursor.execute('''UPDATE avatars SET file = CONCAT("avatar/",SUBSTRING_INDEX(file,"/",-1))''')
        conn.commit()
        cursor.close()
    except Exception as e:
        conn.rollback()

# As there appears to be no way with boto3 to run sync, run subprocess to 'dryrun' sun
# and check that the files were indeed copied over from 1 bucket to the other.
# If there is an error, it will fail, printing the results of files that will
# need to be copied over, and 'migration failed' 3x

# TODO: Do the same against the DB (run a select against the old data and report if there is old data

def checkdata(): 
    proc = subprocess.run(['aws', 's3', 'sync', '--dryrun', 's3://jaysons-legacy-image-bucket/image', 's3://jaysons-new-image-bucket/avatar'], encoding='utf-8', stdout=subprocess.PIPE)

    if 'dryrun' in proc.stdout:
        print(proc.stdout)
        print ("Migration Failed!")
        print ("Migration Failed!")
        print ("Migration Failed!")
    else:
        print ("Migration Successful!")


migratedata()
checkdata()

# Close the Database
conn.close()
