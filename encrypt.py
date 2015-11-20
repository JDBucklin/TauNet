import os
import sys
IV_LENGTH = 10 #lenth of IV
REPS = 10
KEY = 'asdfg'

def main():
   filename = sys.argv[1]
   a_file = open(filename, 'r')
   string = 'I eat onions while I sleep.'
   #encrypted = encrypt(string, 200, 'dookie')
   encrypted = a_file.readline().rstrip()
   decrypted = decrypt(encrypted, REPS, KEY)
   print "This is the starting message: " + string
   print "This is the encrypted message: " + encrypted
   print "This is the decrpted message: " + decrypted

#RC4 Cipher
#length: the length of the message to be encypted
#rounds: the # of rounds to run the key scheduler
#key: the encryption key
def rc4(length, rounds, key):
   key_len = len(key)
   
   #key scheduling done reapeated the for the quantity of rounds specified
   #create a list of 256 bytes
   s = range(0, 256)
   j = 0
   for t in range(0, rounds):
      for i in range(0, 256):
         j = (j + s[i] + ord(key[i % key_len])) % 256
	 s[i], s[j] = s[j], s[i]

   #produce the keystream
   keystream = []
   for i in range(0, 256):
      keystream.append(0)

   j = 0
   t = 0
   for i in range(0, length):
      t = (i + 1) % 256
      j = (j + s[t]) % 256
      s[t], s[j] = s[j], s[t]
      keystream[i] = s[(s[t] + s[j]) % 256]

   return keystream
      
#CipherSaber-2 decryption
#message: the message being decrypted. It should be a message encrypted using RC4.
#rounds: the # of rounds to run the key scheduler for
#key: the encryption key used to encrypt the message
def decrypt(message, rounds, key):
   message_len = len(message)
   iv = message[0:10]
   message = message [10:]
   print "iv: " + iv
   key = key + iv
   print 'key + iv: ' + key
   keystream = rc4(message_len - 10, rounds, key)
   plaintext = ''
   for i in range(0, message_len - 10):
      plaintext += chr(ord(message[i]) ^ keystream[i])
   return plaintext

#CipherSaber-2 encryption
#message: the message being encrypted. It will be encrypted using the RC4 cipher
#rounds: the # of rounds to run the key scheduler for
#key: the encryption key used to encrypt the message.
def encrypt(message, rounds, key):
   message_len = len(message)
   iv = os.urandom(IV_LENGTH)
   key = key + iv
   keystream = rc4(message_len, rounds, key)
   ciphertext = ''
   ciphertext += iv
   for i in range(0, message_len):
      ciphertext += chr(ord(message[i]) ^ keystream[i])
   return ciphertext


main()

