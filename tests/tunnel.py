#!/usr/bin/env python3

#
# Initiate a Tunnel to the MariaDB server in order to perform maintenance
# Replace ssh_address_or_host with the internal address (or hostname)
# of the server/service

import argparse
import paramiko

from sshtunnel import SSHTunnelForwarder

# Arg Parser commands
parser = argparse.ArgumentParser()

parser.add_argument('-r', type=str, required=True,
       help="IP Address of Database Server")
args = parser.parse_args()

ssh_address_or_host= args.r

# SSH Tunnel Data - Pulls ssh_address_or_host from -r in argparse
server = SSHTunnelForwarder(
        (ssh_address_or_host),
         ssh_username="ubuntu",
         ssh_pkey="~/.ssh/id_rsa",
         remote_bind_address=('127.0.0.1',3306),
         local_bind_address=('127.0.0.1',3337)
         )

# Start Server & Print port to screen
server.start()

print(server.local_bind_port)


# We don't want to kill it, but it's here just in case
# server.stop()


