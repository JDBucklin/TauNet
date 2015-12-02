#!/usr/bin/env python

#Copyright (c) 2015 Josh Bucklin
#CS300 - TauNet
#TN_Server.py
#
#This file contains a server implementation for a TauNet node.
#
#It contains a TauNetServer class that enables a user to recieve messages from other
#TauNet nodes within their network. The ability to send messages is implemented
#separately in TN_Client.py.
#
#For more information about TauNet read the included readme.txt that should be
#included with this package.
#
#Files necessary for the operation of this software:
#data.txt - contains info about the username associated with this node and port addresses
#user_table.txt - contains the user table for the TauNet network.
#
#If either of these files is not present please read readme.txt for information about how to get them.
#
#A note about max message length. It is currently specified in TauNet Protocol v0.2 that the max # of
#bytes per message is 1024. The maximum # of bytes in the header section is:
#Header	Space	Payload	Line Ending
#8	1	3	2
#5	1	30	2
#3	1	30	2
#0	1	0	2 <----space in between header and message and trailing newline/return of message
#		Total	91
#which leaves 1024 - 89 = 933 characters that can be used in the actual message.
#these numbers are stored in data.txt.

import socket
import threading
import os, sys, re
from time import sleep
from cs2 import encrypt, decrypt, rc4

#GLOBAL VARIABLES -- VARIABLE NAMES EXPECTED TO NOT BE ASSIGNED ANYWHERE ELSE
mutex = threading.Lock() 

#a TauNet server that allows single messages to be recieved from other TauNet users
#It's important to note that this class makes no aim to eliminate connections from
#users from outside the TauNet network.
class TauNetServer(threading.Thread):
    def __init__(self):
        #mutex is acquired until the server is running. It is realeased in run().
        #this prevents the main loop from being started until the server it started.
        mutex.acquire()
        self.key = ''
        self.welcome()
        threading.Thread.__init__(self)
        self.running = True
        self.known_addresses = []
        self.user_table = {}

        #load class data from local files user_table.txt and data.txt
        self.load_users()
        self.load_data()

    def load_users(self):
        try:
            a_file = open('user_table.txt', 'r')
            for line in a_file:
                line = line.rstrip().split('|')
                if(not re.match('^[A-Za-z0-9-]{3,30}$',line[0])):
                    continue
                self.user_table.update({line[0]:line[1]})
                self.known_addresses.append(socket.gethostbyname(line[1]))
            a_file.close()
        except:
            print 'There was an error reading user_table.txt'
            sys.exit(0)

    def load_data(self):
        #get program data from data.txt
        try:
            a_file = open('data.txt', 'r')
            self.name = a_file.readline().rstrip()
            self.port = int(a_file.readline())
            self.rounds = int(a_file.readline())
            self.version = a_file.readline().rstrip()
            self.max_header = int(a_file.readline())
            self.max_message = int(a_file.readline())
            a_file.close()
        except:
            print 'There was an error reading data.txt'
            sys.exit(0)
    
    def run(self):
        host = '' #generic '' allows connections from any host
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind((host, self.port))
            mutex.release()
        except socket.error, msg:
            print '\nBind failed. Error Code: ' + str(msg[0]) + ' Message: ' + str(msg[1])
            print 'Another instance of TauNet might be running on this computer.'
            print 'Close any other sessions and restart TauNet.'
            mutex.release()
            return False        

        #start server and listen for connections
        server_socket.listen(10)
        while self.running:
            conn, addr = server_socket.accept()
            ciphertext = conn.recv(self.max_message)
            conn.close()
            
            #display a message in its own thread so that more connections can be made
            threading.Thread(target = self.display_message, args = (ciphertext, addr)).start()

        server_socket.close()

    #allows the user to display all users of their network
    def display_users(self):
        mutex.acquire()
        print 'User Table:\n' + 'User Name'.ljust(15) + 'IP'.ljust(10)
        for user in self.user_table:
            print user.ljust(15) + self.user_table[user].ljust(10)
        print ''
        mutex.release()
        
    def set_key(self):
        mutex.acquire()
        self.key = raw_input('Enter an encryption key to use for this session: ')
        mutex.release()

    #takes cipher text, decrypts it and displays it on the screen
    #address is the IP of the sender. If it's not a known sender the user is warned.
    #also if the senders TauNet version is different a warning is displayed
    def display_message(self, ciphertext, address):
        plaintext = decrypt(ciphertext, self.rounds, self.key)
        mutex.acquire()
        if(address[0] not in self.known_addresses):
            print 'WARNING: This message came from an unknown user with IP: ' + address[0]
        if(self.version not in plaintext.split('\r\n')[0]):
            print 'WARNING: The sending user is using a different version of TauNet.'
        print plaintext
        mutex.release()

    #displays the help menu for the server
    def display_usage(self):
        mutex.acquire()
        print '\n--Help Menu--'
        print 'Type exit and press enter to exit'
        print 'Type key and press enter to set a new key'
        print 'Type view to view TauNet users in your network\n'
        mutex.release()

    #waits for input from the user and executes approriate commands
    def menu(self):
        choice = ''
        while(choice != 'exit'):
            choice = raw_input()
            if(choice == 'help'):
                self.display_usage()
            if(choice == 'key'):
                self.set_key()
            if(choice == 'view'):
                self.display_users()

    #displays a welcome message when the server is started
    def welcome(self):
        clear_screen()
        print 'Welcome to your TauNet Server'
        print 'Messages from other users within your TauNet network will'
        print 'appear as they are recieved. If you would like to send messages'
        print 'back to them please use the TauNet client included separately.\n'

        self.key = raw_input('Enter an encryption key to use for this session: ')

        print '\nType help for usage instructions.'
        print 'Now awaiting incoming messages.\n'


def clear_screen():
    for i in range(0, 100):
        print ''
    
def main():
    #create the server and start it
    #if the server failed to start then the program is stopped.
    a_server = TauNetServer()
    a_server.setDaemon(True)
    a_server.start()

    #this mutex is waiting for the server to release the mutex once it has started
    mutex.acquire()
    if(not a_server.isAlive()):
        sys.exit()
    mutex.release()

    #wait for user to exit
    a_server.menu()
    
if __name__ == '__main__':
    main()
