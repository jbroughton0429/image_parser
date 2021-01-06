#!/usr/bin/python3

# Maintenance Script: LS
#
# This Script is a peace of mind script for testing purposes.
# It will go to the 2 buckets defined in 'vars' and list
# the bucket contents to screen


import boto3

# Vars for S3 Buckets
legacy_bucket = "jaysons-legacy-image-bucket"
modern_bucket = "jaysons-new-image-bucket"

# Connect to legacy bucket print results
def remote_ls_legacy(rmls):
        session = boto3.Session()
        s3 = session.resource('s3')
        bucket = s3.Bucket(legacy_bucket)

        for obj in bucket.objects.all():
            names = [bucket.name,obj.key]
            print(names)

# Connect to modern bucket and print results
def remote_ls_modern(rmls):
        session = boto3.Session()
        s3 = session.resource('s3')
        bucket = s3.Bucket(modern_bucket)

        for obj in bucket.objects.all():
            names = [bucket.name,obj.key] 
            print(names)

remote_ls_legacy('rmls')
remote_ls_modern('rmls')


