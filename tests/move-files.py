#!/usr/bin/env python3

# Shamelessly plucked the bucket-to-bucket migration from:
# https://stackoverflow.com/questions/43458001/can-we-copy-the-files-and-folders-recursively-between-aws-s3-buckets-using-boto3

import boto3
import mariadb

s3 = boto3.resource('s3')

bucket = {
        "legacy": "jaysons-legacy-image-bucket", 
        "modern": "jaysons-new-image-bucket"
        }
prefix = {
        "old": 'image',
        "modern": 'avatar'
        }
old_bucket = s3.Bucket(bucket["legacy"])
new_bucket = s3.Bucket(bucket["modern"])


try: conn = mariadb.connect(
		user="rtrenneman",
		password="haveyouturneditoffandonagain",
		host="127.0.0.1",
		port=3337,
		database="avatar_db"
	)
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
	
def myfunction():
    
    cursor = conn.cursor()

    for obj in old_bucket.objects.filter(Prefix=prefix["old"]):
        old_source = { 'Bucket': bucket["legacy"],
                    'Key': obj.key}
        new_key = obj.key.replace(prefix["old"], prefix["modern"], 1)
        new_obj = new_bucket.Object(new_key)
        new_obj.copy(old_source)

    try: 
        cursor.execute("UPDATE avatars SET bucket = replace(bucket,%s,%s)",(bucket["legacy"],bucket["modern"]))
        cursor.execute('''UPDATE avatars SET file = CONCAT("avatar/",SUBSTRING_INDEX(file,"/",-1))''')
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        conn.rollback()

myfunction()
