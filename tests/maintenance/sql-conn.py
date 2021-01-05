#!/usr/bin/python3

# Maintenance Script: SQL Connector
#
# This is a peace of mind test script to validate that the
# SSH Tunnel is operating properly, the credentials are working,
# database is in place and I can see the table.
#

import mariadb
import sys

# Connect to MariaDB Platform
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

cursor = conn.cursor()

# Test to see if I can describe the table
cursor.execute("DESCRIBE avatars")

myresult = cursor.fetchall()

for x in myresult:
    print(x)

cursor.close()
conn.close()
