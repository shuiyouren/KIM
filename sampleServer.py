#!/usr/bin/python
# -*- coding: utf-8 -*-

from kimServer import *

server_port = 5333
server_name = 'kimly.org'
server_host = 'kimly.org'

Server = kimServer (server_port, server_name, server_host )
value = raw_input()
print "Stopping Server"
Server.stop()
print "Stopping stoped?"
