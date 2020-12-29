#!/bin/bash
## Build Keys
mkdir ../keys
cd ../keys
ssh-keygen -t rsa -N "" -f console
ssh-keygen -t rsa -N "" -f database

puttygen console -o console.ppk
puttygen database -o database.ppk
