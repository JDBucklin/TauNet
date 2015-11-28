#Copyright (c) 2015 Josh Bucklin
#CS300 - TauNet
#TN_Client.py
#
#This file contains a client implementation for a TauNet node.
#
#It contains a TauNetClient class that enables a user to send messages to other
#TauNet nodes within their network. The ability to recieve messages is implemented
#separately in TN_Server.py.
#
#For more information about TauNet read the included readme.txt that should be
#included with this package.
#
#Files necessary for the operation of this software:
#data.txt - contains info about the username associated with this node and port addresses
#user_table.txt - contains the user table for the TauNet network.
#
#If either of these files is not present please read readme.txt for information about how to get them.

import socket
import threading
import os, sys, re
from time import sleep
from cs2 import encrypt, decrypt, rc4

#A class that acts as a interface to send/recieve messages to/from other users within a TauNet network.
class TauNetClient():
    def __init__(self):
        #open info file and get self.name, version, port and # rounds for keystream
        try:
            a_file = open('data.txt', 'r')
            self.name = a_file.readline()
            self.port = int(a_file.readline())
            self.rounds = int(a_file.readline())
            self.version = a_file.readline()
            a_file.close()
        except:
            print 'An error occured while reading data.txt.'
            sys.exit(0)
            
        
        #read contents in from local file user_table.txt as the contents are read it only
        #adds usernames that meet the TauNet protocol requirements.
        try:
            self.user_table = {}
            a_file = open('user_table.txt', 'r')
            for line in a_file:
                line = line.rstrip().split('|')
                if(not re.match('^[A-Za-z0-9-]{3,30}$',line[0])):
                   continue
                self.user_table.update({line[0]:line[1]})
            a_file.close()
        except:
            print 'An error occured while reading user_table.txt'
            sys.exit(0)

        #welcome the user and get encryption key from the user
        clear_screen()
        self.welcome()

    #a function that welcomes the user and gets key value for session
    def welcome(self):
        print 'Welcome to your TauNet Client'
        print 'With this program you will be able to send messages to other'
        print 'users within your TauNet network. If you would like to recieve'
        print 'messages please open the TauNet server which should be included'
        print 'separately.\n'

        print 'Follow the prompts at the menu to perform actions. Enjoy!\n'

        self.key = raw_input('Enter the encryption key for this session: ')
        
    #main loop of the program that gives the user options to view/send messages,
    #view the user table, and exit
    def menu(self):
        choice = ''
        while(choice != '0'):
            print 'Choose from the following: '
            print '1 - Send a message to a TauNet user'
            print '2 - View users in your TauNet network'
            print '3 - Set new encryption key for session'
            print '0 - Exit the program'
            choice = raw_input('Enter the # corresponding to your choice: ')
            if(choice == '1'):
                print 'You chose to send a message to another TauNet user.'
                self.send_message()
            elif(choice == '2'):
                print 'You chose to view users in your network.'
                self.display_users()
            elif(choice == '3'):
                print 'You chose to set a new encryption key'
                self.key = raw_input('Enter new encryption key: ')
                self.server.set_key(self.key)
            elif(choice == '0'):
                print 'You chose to exit. Goodbye.'
            else:
                print 'Invalid input. Try again.'
                
            raw_input('Press Enter to Continue')
            clear_screen()
        

    #displays contents of user table stored in self.user_table
    def display_users(self):
        print 'User Table:\n' + 'User Name'.ljust(15) + 'IP'.ljust(10)
        for user in self.user_table:
            print user.ljust(15) + self.user_table[user].ljust(10)

    #makes a connection to a TauNet node of the user's choosing and sends an encrypted
    #message to the selected TauNet node
    def send_message(self):
        #get a valid username of recipient and message from the user
        user = ''
        valid = False
        while(not valid and user != 'cancel'):
            self.display_users()
            user = raw_input('Who would you like to send a message to? (type cancel return to main menu): '
            if(user != 'cancel' and user not in self.user_table.keys()):
                raw_input('Invalid User Name. Try again.')
                clear_screen()
                continue
            valid = True

        message = raw_input('Enter a message to send ' + user + ': ')

        plaintext = 'version: ' + self.version + '\nfrom: ' + self.name + '\nto: ' + user + '\n\n' + message
        ciphertext = encrypt(plaintext, self.rounds, self.key)

        #establish a connection and send message to user if it doesn't finish after
        #5 seconds break the connection.
        try:
            client_socket = socket.create_connection((socket.gethostbyname(self.user_table[user]), self.port), 5)
            client_socket.sendall(ciphertext)
            print 'Message sent successfully!'
        except socket.error, exc:
            print 'User unavailable. Message failed to send.'

def clear_screen():
    for i in range(0,100):
        print ''

def main():
    a_client = TauNetClient()
    a_client.menu()

if __name__ == '__main__':
    main()
