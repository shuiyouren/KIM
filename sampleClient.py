#!/usr/bin/python
# -*- coding: utf-8 -*-

from kimClient import *
import string

server_port = 5333
supernode_port = 5334
server_name = 'kimly.org'
#server_host = 'kimly.org'
server_host = 'localhost'
supernode_host = 'localhost'

print "User?: Eibriel"
username = 'eibriel'
print "Pass?:"
password='eibriel'

print "Loading Supernode"

Supernode = kimSupernode (supernode_port, server_port, server_name, server_host, username, password )
Node = kimNode (supernode_port, supernode_host, server_port, server_name, server_host, username, password )

def onBuddyChange(buddy, action, value):
    '''Buddy changing'''
    print "New status %s %s: %s" % (buddy, action, value)

def onMessageReceiving(from_, to, body, type_):
    '''Message Receiving'''
    print "Message %s from %s to %s: %s" % (type_, from_, to, body)

Node.handleOnBuddyChange ( onBuddyChange )
Node.handleOnMessageReceiving ( onMessageReceiving )

value = ''
while 1:
    value = raw_input("@%s :" % username)
    if value == '': continue
    if value == '!exit': break
    #print value[0]
    if value[0] == '@':
        #print "Mess"
        to = string.split( value, ' ', 1 )[0][1:]
        message = string.split( value, ' ', 1 )[1]
        Node.sendMessage( to, message)
    #Node.send()

print "Stopping Supernode"
Supernode.stop()
print "Supernode stoped?"
