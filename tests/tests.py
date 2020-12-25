#!/usr/bin/env python

""" 

  Initiate a Tunnel to the MiriaDB server in order to perform maintenance
  Replace ssh_address_or_host with the internal address (or hostname) 
  of the server/service

"""
import stunnel

from sshtunnel import SSHTunnelForwarder

ssh_address_or_host= "172.31.36.45"

server = SSHTunnelForwarder(
         (ssh_address_or_host),
         ssh_username="ubuntu",
         ssh_pkey="~/.ssh/id_rsa",
         remote_bind_address=('127.0.0.1',3306),
         local_bind_address=('127.0.0.1',3337)
         )

server.start()

print(server.local_bind_port)

# server.stop()

