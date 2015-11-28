#Copyright (c) 2015 Josh Bucklin
#CS300 - TauNet
#This file contains an implementation of CipherSaber-2 which uses RC4.
#
#More information about CipherSaber-2 can be found on wikipedia here: https://en.wikipedia.org/wiki/CipherSaber
#
#Additionally this implementation is based off of Bart Massey's implementation which can
#be found on his GitHub account here: https://github.com/BartMassey/ciphersaber2

import os
import sys

#RC4 Cipher - This function creates a keystream that corresponds to the length
#of a message that is being encrypted/decrypted.
#length: the length of the message to be encrypted/decrypted
#rounds: the # of rounds to run the key scheduler. should be a minimum of 20
#key: the encryption key
def rc4(length, rounds, key):
   key_len = len(key)
   
   #key scheduling repeated for the quantity of rounds specified
   #create a list of 256 bytes
   state = range(0, 256)
   j = 0
   for t in range(0, rounds):
      for i in range(0, 256):
         j = (j + state[i] + ord(key[i % key_len])) % 256
	 state[i], state[j] = state[j], state[i]

   #produce the keystream
   keystream = []
   j = 0
   for i in range(0, length):
      t = (i + 1) % 256
      j = (j + state[t]) % 256
      state[t], state[j] = state[j], state[t]
      keystream.append(state[(state[t] + state[j]) % 256])

   return keystream
      
#CipherSaber-2 decryption.
#message: the message being decrypted. It should be a message encrypted using RC4.
#rounds: the # of rounds to run the key scheduler for
#key: the encryption key used to encrypt the message
def decrypt(message, rounds, key):
   #remove the IV from the ciphertext
   message_len = len(message)
   iv_length = 10
   iv = message[0:iv_length]
   message = message [iv_length:]

   #create the cipher key by appending the recieved IV to the passed key
   #generate the keystream and decrypt the message
   key = key + iv
   keystream = rc4(message_len - iv_length, rounds, key)
   plaintext = ''
   for i in range(0, message_len - iv_length):
      plaintext += chr(ord(message[i]) ^ keystream[i])
   return plaintext

#CipherSaber-2 encryption
#message: the message being encrypted. It will be encrypted using the RC4 cipher
#rounds: the # of rounds to run the key scheduler for
#key: the encryption key used to encrypt the message.
def encrypt(message, rounds, key):
   #generate a random iv to append to the passed key
   iv_length = 10
   iv = os.urandom(iv_length)
   key = key + iv

   #create the keystream and encrypt the ciphertext by first adding the iv 
   #to it for decryption and then appending the ciphertext
   message_len = len(message)
   keystream = rc4(message_len, rounds, key)
   ciphertext = ''
   ciphertext += iv
   for i in range(0, message_len):
      ciphertext += chr(ord(message[i]) ^ keystream[i])
   return ciphertext


def test():
   a_file = open(sys.argv[1], 'r')
   #encrypted = a_file.read().rstrip()
   #message = 'I eat onions while I sleep'
   message = ''
   encrypted = encrypt(message, 10, 'asdfg')
   decrypted = decrypt(encrypted, 10, 'asdfg')
   print 'this is the starting: ' + message
   print sys.getsizeof(message)
   print sys.getsizeof(encrypted)
   print sys.getsizeof(decrypted)
   print 'this is the encrypted message: ' + encrypted
   print 'this is the decrypted message: ' + decrypted

if __name__ == '__main__':
   test()


