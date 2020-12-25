#!/bin/bash
## Build Keys
mkdir ../keys
ssh-keygen -t rsa -N "" -f ../keys/console
ssh-keygen -t rsa -N "" -f ../keys/database

