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

#A class that acts as a interface to send/recieve messages to/from
#other users within a TauNet network.
#It includes an instance of a TauNetServer that is started immmeadiately within a separate thread
class TauNet():
    def __init__(self):
        self.server = TauNetServer()
        self.server.setDaemon(True)
        self.server.start()
        self.user_table = {}
        
        #read contents in from local file user_table.txt
        a_file = open('user_table.txt', 'r')
        for line in a_file:
            line = line.rstrip().split('|')
            self.user_table.update({line[0]:line[1]})

        a_file.close()

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
        
        ciphertext = encrypt('version: ' + VERSION + '\nfrom: ' self.name + '\nto: ' + user + '\n\n' + message)

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
    a_net.send_message()
  
main()
