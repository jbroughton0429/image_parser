#!/usr/bin/env python3
import os
import argparse
import shutil
import boto3

from tempfile import mkstemp

# Vars for bucket storage and temporary files
legacy_dir = "./legacy-s3"
modern_dir = "./production-s3"
legacy_bucket = "jaysons-legacy-image-bucket"
modern_bucket = "jaysons-new-image-bucket"

# ArgParser Commanders
parser = argparse.ArgumentParser()

parser.add_argument('-d', nargs="+", default=["legacy-s3","production-s3"],
        help="Delete Files no longer in use - default: legacy-s3, production-s3")

args = parser.parse_args()

avatar_dirs = args.d

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


