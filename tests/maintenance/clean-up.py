#!/usr/bin/env python3

# Maintenance Script: DELETE
#
# This Script will do the following items:
#
# * Delete all items in 2 buckets with the following prefix: avatar*
# * Delete the 2 temp files 'legacy' and 'modern' in the filesystem
#* Truncate the Avatars table in the avatar_db
#

import shutil
import boto3
import mariadb

s3 = boto3.resource('s3')

# Vars for bucket storage and temporary files
bucket = {
        "legacy": "jaysons-legacy-image-bucket",
        "modern": "jaysons-new-image-bucket"
        }

old_bucket = s3.Bucket(bucket["legacy"])
new_bucket = s3.Bucket(bucket["modern"])

avatar_dirs = ["../image","../avatar"]

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


def remote_del_legacy():
    '''
    Delete all Tempotary S3 Bucket data 'image' after testing

    TODO (Maybe) Roll old/new buckets and prefix var's into a tuple. Then merge remote_del_legacy and remote_del_modern as single function

    TODO - Error handling in Delete is missing
    '''
    session = boto3.Session()
    bucket = old_bucket

    for obj in bucket.objects.filter(Prefix='image'):
        s3.Object(bucket.name, obj.key).delete()

def remote_del_modern():
    '''
    Delete all Temporary S3 Bucket data 'avatar' after testing
    '''
    session = boto3.Session()
    bucket = new_bucket

    for obj in bucket.objects.filter(Prefix='avatar'):
        s3.Object(bucket.name, obj.key).delete()


def remote_maria():
    '''
    Drop all data in avatar table
    '''
    cursor = conn.cursor()
    cursor.execute('TRUNCATE TABLE avatars;')
    conn.commit()
    cursor.close()
    conn.close()

# Run Everything
remote_del_legacy()
remote_del_modern()
remote_maria()
