import socket
import threading
import os
from cs2 import encrypt, decrypt, rc4

#globals -- should not be changed -- consider to be constants
PORT = 6283
VERSION = '0.1'

#a TauNet server that allows single messages to be recieved
class TauNetServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True

    def run(self):
        host = '' #generic '' allows connections from any host

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server_socket.bind((host, PORT))
        except socket.error, msg:
            print 'Bind failed. Error Code: ' + str(msg[0]) + ' Message: ' + str(msg[1])

        server_socket.listen(10)
        while self.running:
            conn, addr = server_socket.accept()
            data = conn.recv(1024)
            conn.close()

        server_socket.close()

#A class that acts as a interface to send/recieve messages to/from other users within a TauNet network.
#It includes an instance of a TauNetServer that is started immmeadiately within a separate thread
class TauNet():
    def __init__(self):
        self.server = TauNetServer()
        self.server.setDaemon(True)
        self.server.start()
        self.user_table = {}
        self.name = ''
        
        #the first line of the user_table.txt file corresponds to the owner of the TauNet
        a_file = open('user_table.txt', 'r')
        self.name = a_file.readline().split('|')[0]
        a_file.close()
        
        #read contents in from local file user_table.txt
        a_file = open('user_table.txt', 'r')
        for line in a_file:
            line = line.rstrip().split('|')
            self.user_table.update({line[0]:line[1]})

        a_file.close()

    #main loop of the program
    #gives the user options to view/send messages, view user table, and exit
    def menu(self):
        choice = 999
        while(choice != 0):
            print 'Choose from the following: '
            print '1 - Send a message to a TauNet user'
            print '2 - Check for messages recieved from other TauNet users'
            print '3 - View users in your TauNet network'
            print '0 - Exit the program'
            choice = int(raw_input('Enter the # corresponding to your choice: '))
            if(choice == 1):
                print 'You chose to send a message to another TauNet user.'
                self.send_message()
            else if(choice == 2):
                print 'You chose to check your messages.'
            else if(choice == 3):
                print 'You chose to view users in your network.'
                self.display_users()
            else if(choice == 0):
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
        
        ciphertext = encrypt('version: ' + VERSION + '\nfrom: ' + self.name + '\nto: ' + user + '\n\n' + message)

        #establish a connection and send message to user
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((self.user_table[user], PORT))
            client_socket.sendall(message)
            raw_input('Message sent successfully! Press Enter to Continue.')
        except socket.error, exc:
            raw_input('User unavailable. Message failed to send.')
        
#clears screen by outputting 100 lines
def clear_screen():
    for i in range(0, 100):
        print ''

def main():
    a_net = TauNet()
    a_net.menu()
  
main()
