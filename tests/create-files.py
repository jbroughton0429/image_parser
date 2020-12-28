#!/usr/bin/env python
import os
import argparse
import tempfile
import logging
import boto3
import botocore.exceptions 

from tempfile import mkstemp

Working_Dir = "."
legacy_dir = "./legacy-s3"
modern_dir = "./production-s3"

if not os.path.exists(legacy_dir):
    os.mkdir(legacy_dir);

if not os.path.exists(modern_dir):
    os.mkdir(modern_dir);

parser = argparse.ArgumentParser()

parser.add_argument('-l', type=int, required=True,
                help="Number of Legacy files to create")

parser.add_argument('-m', type=int, required=True,
                help="Number of Modern files to create")

args = parser.parse_args()

legacy_num = args.l
modern_num = args.m

for i in range(legacy_num):

    fd, path = mkstemp(prefix='avatar-', suffix='.png', dir=legacy_dir)

    with os.fdopen(fd, 'w') as fp:
        fp.write('Legacy Files\n')
    
    s3 = boto3.client('s3')
    with open(fd, "rb") as f:
        s3.upload_fileobj(f, "jaysons-legacy-image-bucket", fd)

for i in range(modern_num):

    fd, path = mkstemp(prefix='avatar-', suffix='.png', dir=modern_dir)

    with os.fdopen(fd, 'w') as fp:
        fp.write('Modern Files\n')


