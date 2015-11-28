import socket
import threading
import os, sys, re
from time import sleep
from cs2 import encrypt, decrypt, rc4

#a TauNet server that allows single messages to be recieved
class TauNetServer(threading.Thread):
    def __init__(self):
        self.key = ''
        self.welcome()
        threading.Thread.__init__(self)
        self.running = True

        #get port and # of rounds from info.txt
        a_file = open('info.txt', 'r')
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
    #set up server and start it if it fails to start then exit the program
    a_server = TauNetServer()
    a_server.setDaemon(True)
    a_server.start()
    sleep(0.5)
    if(not a_server.isAlive()):
        sys.exit()

    #wait for user to exit
    a_server.menu()
    
if __name__ == '__main__':
    main()
