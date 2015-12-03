#!/usr/bin/env python

#Copyright (c) 2015 Josh Bucklin
#cs2_test.py

#a program to test the general functionality of cs2.py

from cs2 import rc4, encrypt, decrypt
import sys

def in_out_test():
    #variables
    test_string = ''
    enc_string = ''
    dec_string = ''
    key1 = 'pass'
    round1 = 20
    
    print 'INPUT-OUTPUT TESTS'

    #test 1 - empty string
    test_string = ''
    enc_string = encrypt(test_string, round1, key1)
    dec_string = decrypt(enc_string, round1, key1)
    print_result(test_string, dec_string)
    
    #test 2
    test_string = 'abc'
    enc_string = encrypt(test_string, round1, key1)
    dec_string = decrypt(enc_string, round1, key1)
    print_result(test_string, dec_string)
    
    #test 3
    test_string = '1_*()()$*'
    enc_string = encrypt(test_string, round1, key1)
    dec_string = decrypt(enc_string, round1, key1)
    print_result(test_string, dec_string)
    
    #test 4
    test_string = 'I ate a waffle on my dogs 15th birthday!'
    enc_string = encrypt(test_string, round1, key1)
    dec_string = decrypt(enc_string, round1, key1)
    print_result(test_string, dec_string)
    
    #test 5
    test_string = 'marSHmallow SQuare$'
    enc_string = encrypt(test_string, round1, key1)
    dec_string = decrypt(enc_string, round1, key1)
    print_result(test_string, dec_string)
    
    #test 6
    test_string = 'I love computers!'
    enc_string = encrypt(test_string, round1, key1)
    dec_string = decrypt(enc_string, round1, key1)
    print_result(test_string, dec_string)
    
    #test 7
    test_string = '`123~!@#$%^^&*()_+|}\n\t0'
    enc_string = encrypt(test_string, round1, key1)
    dec_string = decrypt(enc_string, round1, key1)
    print_result(test_string, dec_string)

    #test 8 - protocol line endings
    test_string = '\r\n'
    enc_string = encrypt(test_string, round1, key1)
    dec_string = decrypt(enc_string, round1, key1)
    print_result(test_string, dec_string)

#tests that shouldn't match which still gives a pass
def fail_test():
    #variables
    test_string = ''
    enc_string = ''
    dec_string = ''
    key1 = 'pass'
    key2 = 'word'
    round1 = 20
    round2 = 10

    print '\nFAIL TESTS - THESE ARE SUPPOSED TO FAIL'
    
    #Test 1 - different encrypt and decrypt key
    print 'Test - Different keys'
    test_string = 'This is a test string!'
    enc_string = encrypt(test_string, round1, key1)
    dec_string = decrypt(enc_string, round1, key2)
    print_result(test_string, dec_string)
        
    #Test 2 - different rounds count
    print 'Test - Different Rounds'
    test_string = 'This is a test string!'
    enc_string = encrypt(test_string, round1, key1)
    dec_string = decrypt(enc_string, round2, key1)
    print_result(test_string, dec_string)
        
    #Test 3 - different rounds and keys
    print 'Test - Different rounds/keys'
    test_string = 'This is a test string!'
    enc_string = encrypt(test_string, round1, key1)
    dec_string = decrypt(enc_string, round2, key2)
    print_result(test_string, dec_string)
    
def print_result(before, after):
    print 'String Encryption: ' + before
    print 'String After Decryption: ' + after
    if(before == after):
        print 'Test: PASS'
    else:
        print 'Test: FAIL'

#verifies the # of bytes correct for all levels of encryption
#this project uses 10byte IV so it's expected that encrypt will be
#10 more bytes than both plain and decrypt
def size_verification():
    #variables
    test_string = ''
    enc_string = ''
    dec_string = ''
    key1 = 'pass'
    round1 = 20

    #set a test string and verify sizes
    test_string = 'This is a test string'
    encrypted = encrypt(test_string, round1, key1)
    decrypted = decrypt(encrypted, round1, key1)
    
    print 'Size of original: ' + str(sys.getsizeof(test_string))
    print 'Size of encrypted: ' + str(sys.getsizeof(encrypted))
    print 'Size of decrypted: ' + str(sys.getsizeof(decrypted))

    print test_string
    print encrypted
    print decrypted
    if(sys.getsizeof(test_string) == sys.getsizeof(encrypted) - 10):
        print 'Test Pass'
    else:
        print 'Test Fail'
        
def main():
    in_out_test()
    fail_test()
    size_verification()

if __name__ == '__main__':
    main()
