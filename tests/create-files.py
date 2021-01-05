#!/usr/bin/env python3
import os
import argparse
import tempfile
import logging
import boto3
import botocore.exceptions
import mariadb
import paramiko

from sshtunnel import SSHTunnelForwarder
from tempfile import mkstemp

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

# Create Legacy and Modern Directories if they do not exist
if not os.path.exists(directory["legacy"]):
        os.mkdir(directory["legacy"]);

if not os.path.exists(directory["modern"]):
        os.mkdir(directory["modern"]);

# Creates Temp files on the file system
def temp_files(tempfile):

    for i in range(legacynum):
        fd, path = mkstemp(prefix='avatar-', suffix='.png', dir=directory["legacy"])
        with os.fdopen(fd, 'w') as fp:
            fp.write('Legacy Files\n')


    for i in range(modernnum):
        fd, path = mkstemp(prefix='avatar-', suffix='.png', dir=directory["modern"])
        with os.fdopen(fd, 'w') as fp:
            fp.write('Modern Files\n')

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

conn.close()

