#!/usr/bin/env python3

#
# Core Script: Create Files
#
# This script builds/creates your temporary files used for testing purposes
# We use mkstemp to write a bunch of temp files to the filesystem and then
# move these files over to 2 buckets, using an authorized sql user
# This uses argparse with -l (legacy) and -m (modern) variables to create
# the number of files necessary
#
# When you are done playing around, be sure you run it's companion script
# <clean-up.py> which will delete these folders/temp-files, clear the database
# and the S3 buckets of 'avatar'

import os
import argparse
import tempfile
import boto3
import mariadb

from tempfile import mkstemp

# Declare your Bucket and Directory Vars

directory = {
	"legacy":"image",
	"modern":"avatar"
	}

bucket = {
	"legacy":"jaysons-legacy-image-bucket",
	"modern":"jaysons-new-image-bucket"
	}

s3 = boto3.resource('s3')
old_bucket = s3.Bucket(bucket["legacy"])
new_bucket = s3.Bucket(bucket["modern"])

# SQL Connector - Be sure you use your authorized user (NOT ROOT)

try:
     conn = mariadb.connect(
         user="rtrenneman",
         password="haveyouturneditoffandonagain",
         host="127.0.0.1",
         port=3337,
         database="avatar_db"
        )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Arg Parser commands
parser = argparse.ArgumentParser()

parser.add_argument('-l', type=int, required=True,
                        help="Number of Legacy files to create")

parser.add_argument('-m', type=int, required=True,
                        help="Number of Modern files to create")

args = parser.parse_args()

legacynum = args.l
modernnum = args.m

# Create Legacy and Modern Directories on this FS if they do not exist

if not os.path.exists(directory["legacy"]):
        os.mkdir(directory["legacy"]);

if not os.path.exists(directory["modern"]):
        os.mkdir(directory["modern"]);

# Creates Temp files on this FS

def temp_files(tempfile):

    for i in range(legacynum):
        fd, path = mkstemp(prefix='avatar-', suffix='.png', dir=directory["legacy"])
        with os.fdopen(fd, 'w') as fp:
            fp.write('Legacy Files\n')


    for i in range(modernnum):
        fd, path = mkstemp(prefix='avatar-', suffix='.png', dir=directory["modern"])
        with os.fdopen(fd, 'w') as fp:
            fp.write('Modern Files\n')

# Upload Legacy and Modern Data from Temp FS to the respective Buckets;
# Push this data into the Database
# TODO - Error Handling
def upload_legacy_files(path):
    bucket = old_bucket
    cursor = conn.cursor()

    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
               bucket.put_object (Key=full_path, Body=data)
        for obj in bucket.objects.all():
            names = [bucket.name,obj.key]
            sql = "INSERT INTO avatars (bucket, file) VALUES (%s, %s)"
            cursor.execute(sql, names)
    conn.commit()
    cursor.close()

def upload_modern_files(path):
    bucket = new_bucket
    cursor = conn.cursor()

    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
                bucket.put_object (Key=full_path, Body=data)
        for obj in bucket.objects.all():
            names = [bucket.name,obj.key]
            sql = "INSERT INTO avatars (bucket, file) VALUES (%s, %s)"
            cursor.execute(sql, names)
    conn.commit()
    cursor.close()

temp_files('tempfile')
upload_legacy_files(directory["legacy"])
upload_modern_files(directory["modern"])

# Close the Database Connection
conn.close()

