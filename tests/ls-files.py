#!/usr/bin/python

import os, sys

# Open file
path = "./legacy-s3"
dirs = os.listdir( path )

for file in dirs:
    print (file)

