#!/usr/bin/env python3
import os
import argparse
import tempfile
import logging
import boto3
import botocore.exceptions
import mariadb

from tempfile import mkstemp

# Temp directory for temporary file storage
Working_Dir = "."
legacy_dir = "image"
modern_dir = "avatar"
legacy_bucket = "jaysons-legacy-image-bucket"
modern_bucket = "jaysons-new-image-bucket"

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

legacy_num = args.l
modern_num = args.m

# Create Legacy and Modern Directories if they do not exist
if not os.path.exists(legacy_dir):
        os.mkdir(legacy_dir);

if not os.path.exists(modern_dir):
        os.mkdir(modern_dir);

# Creates Temp files on the file system
def temp_files(tempfile):

    for i in range(legacy_num):

        fd, path = mkstemp(prefix='avatar-', suffix='.png', dir=legacy_dir)

        with os.fdopen(fd, 'w') as fp:
            fp.write('Legacy Files\n')


    for i in range(modern_num):

        fd, path = mkstemp(prefix='avatar-', suffix='.png', dir=modern_dir)

        with os.fdopen(fd, 'w') as fp:
            fp.write('Modern Files\n')

temp_files('tempfile')

def upload_legacy_files(path):
    session = boto3.Session()
    s3 = session.resource('s3')
    bucket = s3.Bucket(legacy_bucket)
    remoteDirectoryName = "image"
    mycursor = conn.cursor()

    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
               bucket.put_object (Key=full_path, Body=data)
        for obj in bucket.objects.all():
            names = [bucket.name,obj.key]
            sql = "INSERT INTO avatars (bucket, file) VALUES (%s, %s)"
            mycursor.execute(sql, names)
    conn.commit()

def upload_modern_files(path):
    session = boto3.Session()
    s3 = session.resource('s3')
    bucket = s3.Bucket(modern_bucket)
    mycursor = conn.cursor()

    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
                bucket.put_object (Key=full_path, Body=data)
        for obj in bucket.objects.all():
            names = [bucket.name,obj.key]
            sql = "INSERT INTO avatars (bucket, file) VALUES (%s, %s)"
            mycursor.execute(sql, names)

    conn.commit()


upload_legacy_files(legacy_dir)
upload_modern_files(modern_dir)

