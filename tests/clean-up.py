#!/usr/bin/env python
import os
import argparse
import shutil

from tempfile import mkstemp

parser = argparse.ArgumentParser()

parser.add_argument('-d', nargs="+", default=["legacy-s3","production-s3"],
        help="Delete Files no longer in use - default: legacy-s3, production-s3")

args = parser.parse_args()

avatar_dirs = args.d

for x in avatar_dirs:
    shutil.rmtree(x, ignore_errors=True)
