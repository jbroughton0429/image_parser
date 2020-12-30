#!/usr/bin/env python3
import os
import argparse
import shutil
import boto3
import mariadb

from tempfile import mkstemp

# Vars for bucket storage and temporary files
legacy_dir = "../legacy-s3"
modern_dir = "../production-s3"
legacy_bucket = "jaysons-legacy-image-bucket"
modern_bucket = "jaysons-new-image-bucket"

# ArgParser Commanders
parser = argparse.ArgumentParser()

parser.add_argument('-d', nargs="+", default=["../legacy-s3","../production-s3"],
        help="Delete Files no longer in use - default: legacy-s3, production-s3")

## I need to add this to argparse -
#parser.add_argument('-m', '--simulate', action='store_true',
#                        help="Wipe Remote MariaDB database")


args = parser.parse_args()

avatar_dirs = args.d
#remote_maria = args.m

# MariaDB Connector

try:
	conn = mariadb.connect(
		user="root",
		password="supersecretsquirrel",
		host="127.0.0.1",
		port=3337,
		database="avatar_db"
	)
except mariadb.Error as e:
	print(f"Error connecting to MariaDB Platform: {e}")
	sys.exit(1)

# Delete temp filesystem directories

for x in avatar_dirs:
    shutil.rmtree(x, ignore_errors=True)


# Whack all Temporary S3 Bucket data 'avatar' after testing
def remote_del_legacy(remwhack):
    session = boto3.Session()
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(legacy_bucket)

    for obj in bucket.objects.filter(Prefix='avatar'):
            s3.Object(bucket.name, obj.key).delete()

def remote_del_modern(remwhack):
    session = boto3.Session()
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(modern_bucket)

    for obj in bucket.objects.filter(Prefix='avatar'):
        s3.Object(bucket.name, obj.key).delete()

remote_del_legacy('remwhack')
remote_del_modern('remwhack')

# Whack the database
def remote_maria(remote_db):
	mycursor = conn.cursor()
	mycursor.execute('TRUNCATE TABLE avatars;')
	conn.commit()
remote_maria('remote_db')
