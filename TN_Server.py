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

#used to prevent multiple functions from printing to the screen at the same time
mutex = threading.Lock() 

#a TauNet server that allows single messages to be recieved from other TauNet users
#as a precaution before use it's important to note that this class makes no aim to
#eliminate connections from users from outside the TauNet network.
class TauNetServer(threading.Thread):
    def __init__(self):
        #acquire the mutex until the server is running. this provides a way to ensure
        #that the server is started properly before giving the user options of what to do.
        #this mutex is released in the run() function after the server is started.
        mutex.acquire()
        self.key = ''
        self.welcome()
        threading.Thread.__init__(self)
        self.running = True

        #get port and # of rounds from data.txt
        a_file = open('data.txt', 'r')
        self.name = a_file.readline()
        self.port = int(a_file.readline())
        self.rounds = int(a_file.readline())
        self.version = a_file.readline()
        a_file.close()
        
    def run(self):
        host = '' #generic '' allows connections from any host
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind((host, self.port))
        except socket.error, msg:
            print '\nBind failed. Error Code: ' + str(msg[0]) + ' Message: ' + str(msg[1])
            print 'Another instance of TauNet might be running on this computer.'
            print 'Close any other sessions and restart TauNet.'
            return False
        finally:
            mutex.release()
        

        #start server and listen for connections
        server_socket.listen(10)
        while self.running:
            conn, addr = server_socket.accept()
            ciphertext = conn.recv(1024)
            conn.close()
            print decrypt(ciphertext, self.rounds, self.key)

        server_socket.close()

    def set_key(self, key):
        self.key = key

    #waits for input from the user and executes approriate commands
    def menu(self):
        choice = '0'
        while(choice != 'exit'):
            choice = raw_input()

    #displays a welcome message when the server is started
    def welcome(self):
        clear_screen()
        print 'Welcome to your TauNet Server'
        print 'Messages from other users within your TauNet network will'
        print 'appear as they are recieved. If you would like to send messages'
        print 'back to them please use the TauNet client included separately.\n'

        self.key = raw_input('Enter an encryption key to use for this session: ')

        print 'Thank you. Now awaiting incoming messages.\n'
        print 'If you would like to stop the server type exit and press enter.\n'


def clear_screen():
    for i in range(0, 100):
        print ''
    
def main():
    #create server and start it
    #if the server failed to start exit the program the mutex is used to prevent
    #the main loop of the program from starting in the event the server fails to start
    a_server = TauNetServer()
    a_server.setDaemon(True)
    a_server.start()

    mutex.acquire()
    if(not a_server.isAlive()):
        sys.exit()
    mutex.release()

    #wait for user to exit
    a_server.menu()
    
if __name__ == '__main__':
    main()
