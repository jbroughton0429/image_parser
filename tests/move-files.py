#!/usr/bin/env python3

# Shamelessly plucked from:
# https://stackoverflow.com/questions/43458001/can-we-copy-the-files-and-folders-recursively-between-aws-s3-buckets-using-boto3


## Jayson Note - move my MySQL SP into this python, less vars in less files to handle on setup.

import boto3

old_bucket_name = 'jaysons-legacy-image-bucket'
old_prefix = 'image'
new_bucket_name = 'jaysons-new-image-bucket'
new_prefix = 'avatar'
s3 = boto3.resource('s3')
old_bucket = s3.Bucket(old_bucket_name)
new_bucket = s3.Bucket(new_bucket_name)

for obj in old_bucket.objects.filter(Prefix=old_prefix):
    old_source = { 'Bucket': old_bucket_name,
                   'Key': obj.key}
    new_key = obj.key.replace(old_prefix, new_prefix, 1)
    new_obj = new_bucket.Object(new_key)
    new_obj.copy(old_source)

