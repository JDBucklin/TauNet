import socket
import threading
from CipherSaber-2 import encrypt, decrypt, RC4

#a TauNet server that allows single messages to be recieved
class TauNetServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True

    def run(self):
        HOST = '' #generic '' allows connections from any host
        PORT = 6283

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server_socket.bind((HOST, PORT))
        except socket.error, msg:
            print 'Bind failed. Error Code: ' + str(msg[0]) + ' Message: ' + str(msg[1])

        server_socket.listen(10)
        while self.running:
            conn, addr = server_socket.accept()
            data = conn.recv(1024)
            #print 'Message recieved from ' + addr[0] + ': ' + data
            conn.close()

        server_socket.close()
        print "Server Stopped Successfully"

    #stops the server and closes the thread.
    #to accomplish this is must make a connection with itself to finish the accept loop
    def stop_server(self):
        self.running = False
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('192.168.1.39', 6283))

#A class that acts as a interface to send/recieve messages to/from
#other users within a TauNet network.
#It includes an instance of a TauNetServer that is started immmeadiately within a separate thread
class TauNet():
    

#a client of the TauNet network
#it stores a list of possible users to send messages to read in from a local file
class TauNetClient():
    def __init__(self):
        self.name = 'jbucklin'

    def send_message(self):
        message = raw_input('Enter a message: ')
        c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #replace this with file search or when client is made it has list available
        HOST = '192.168.1.39'
        PORT = 6283

        #connect to server and send the message
        #server is expected to close the connection
        c_socket.connect((HOST, PORT))
        c_socket.sendall(message)
        print 'Message sent successfully!\n'
        
def main():
    a_server = TauNetServer()
    a_server.start()

    a_client = TauNetClient()
    again = True
    while(again != 'n'):
        a_client.send_message()
        again = raw_input('again?')

    a_server.stop_server()
    a_server.join()
    
main()
