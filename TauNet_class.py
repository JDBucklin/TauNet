import socket
import threading
import os
import sys
import re
import time
from cs2 import encrypt, decrypt, rc4

#a TauNet server that allows single messages to be recieved
class TauNetServer(threading.Thread):
    def __init__(self, port, key, rounds):
        threading.Thread.__init__(self)
        self.running = True
        self.port = port
        self.key = key
        self.messages = []
        self.rounds = rounds
        
    def run(self):
        host = '' #generic '' allows connections from any host

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind((host, self.port))
        except socket.error, msg:
            print 'Bind failed. Error Code: ' + str(msg[0]) + ' Message: ' + str(msg[1])
            print 'Another instance of TauNet might be running on this computer.'
            print 'Close any other sessions an restart TauNet.'
            return False

        #start server and listen for connections
        server_socket.listen(10)
        while self.running:     
            conn, addr = server_socket.accept()
            ciphertext = conn.recv(1024)
            conn.close()
            self.messages.append(decrypt(ciphertext, self.rounds, self.key))

        server_socket.close()

    def set_key(self, key):
        self.key = key

    def display_message(self):
        for message in self.messages:
            print message
        

#A class that acts as a interface to send/recieve messages to/from other users within a TauNet network.
#It includes an instance of a TauNetServer that is started immmeadiately within a separate thread
class TauNet():
    def __init__(self):
        self.version = '0.1'
        self.port = 6283
        self.rounds = 200
        
        #the first line of the user_table.txt file corresponds to the owner of the TauNet
        a_file = open('user_table.txt', 'r')
        self.name = a_file.readline().split('|')[0]
        a_file.close()
        
        #read contents in from local file user_table.txt
        #as the contents are read it only adds usernames that meet the TauNet protocol requirements
        self.user_table = {}
        a_file = open('user_table.txt', 'r')
        for line in a_file:
            line = line.rstrip().split('|')
            if(not re.match('^[A-Za-z0-9-]{3,}$',line[0])):
               continue
            self.user_table.update({line[0]:line[1]})
        a_file.close()

        #get this sessions encryption key from the user
        self.key = raw_input('Enter the encryption key for this session: ')

        #create and start server if the server fails to start abort the program
        #the sleep portion prevents the menu from being shown in the event of bind failure
        self.server = TauNetServer(self.port, self.key, self.rounds)
        self.server.setDaemon(True)
        self.server.start()
        time.sleep(0.5)
        if(not self.server.isAlive()):
            sys.exit()

    #main loop of the program
    #gives the user options to view/send messages, view user table, and exit
    def menu(self):
        choice = ''
        while(choice != '0'):
            print 'Choose from the following: '
            print '1 - Send a message to a TauNet user'
            print '2 - Check for messages recieved from other TauNet users'
            print '3 - View users in your TauNet network'
            print '4 - Set new encryption key for session'
            print '0 - Exit the program'
            choice = raw_input('Enter the # corresponding to your choice: ')
            if(choice == '1'):
                print 'You chose to send a message to another TauNet user.'
                self.send_message()
            elif(choice == '2'):
                print 'You chose to check your messages.'
                self.server.display_message()
            elif(choice == '3'):
                print 'You chose to view users in your network.'
                self.display_users()
            elif(choice == '4'):
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

    #makes a connection to a host of the user's choosing
    #and sends an encrypted message to the selected host
    def send_message(self):
        #get username of recipient and message from the user
        valid = False
        while(not valid):
            self.display_users()
            user = raw_input('Enter the User Name of the person you would like to send a message: ')
            if(user not in self.user_table.keys()):
                raw_input('Invalid User Name. Try again.')
                clear_screen()
                continue
            valid = True

        message = raw_input('Enter a message to send ' + user + ': ')

        plaintext = 'version: ' + self.version + '\nfrom: ' + self.name + '\nto: ' + user + '\n\n' + message
        ciphertext = encrypt(plaintext, self.rounds, self.key)

        #establish a connection and send message to user
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((self.user_table[user], self.port))
            client_socket.sendall(ciphertext)
            print 'Message sent successfully!'
        except socket.error, exc:
            print 'User unavailable. Message failed to send.'
        
#clears screen by outputting 100 lines
def clear_screen():
    for i in range(0, 100):
        print ''

def main():
    a_net = TauNet()
    a_net.menu()

if __name__ == '__main__':
    main()
