#!/usr/bin/python3

# Module Imports
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

mycursor = conn.cursor()

# Test to see if I can describe the table
mycursor.execute("DESCRIBE avatars")

myresult = mycursor.fetchall()

for x in myresult:
    print(x)

