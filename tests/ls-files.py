#!/usr/bin/python3

import boto3

# Vars for S3 Buckets
legacy_bucket = "jaysons-legacy-image-bucket"
modern_bucket = "jaysons-new-image-bucket"

def remote_ls_legacy(rmls):
        session = boto3.Session()
        s3 = session.resource('s3')
        bucket = s3.Bucket(legacy_bucket)

        for obj in bucket.objects.all():
            print(obj.key)

def remote_ls_modern(rmls):
        session = boto3.Session()
        s3 = session.resource('s3')
        bucket = s3.Bucket(modern_bucket)

        for obj in bucket.objects.all():
            print(obj.key)

remote_ls_legacy('rmls')
remote_ls_modern('rmls')


