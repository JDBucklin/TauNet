Copyright (c) 2015 Josh Bucklin
TauNet v1.0

--OVERVIEW--
TauNet is a communication software developed as part of class project for CS300 at Portland State University. The central purpose of this project was to create a means of secure communication across the internet in a small previously established network using a Raspberry Pi 2.

--SECURITY--
TauNet utilizes RC4 and CipherSaber-2 to encrypt its messages. RC4 requires a key to operate. This key is to be used on every node that is in the network. Each time TN_Server.py or TN_Client.py is started it will require the user to enter a key for the session. This is done to increase security and to avoid having the password compromised in the event of theft.

--WHATS INCLUDED--
Included with this package should be the following files:
1. TN_Server.py - This is how a TauNet user will recieve messages from other TauNet nodes

2. TN_Client.py - This is how a TauNet user will send messages to other TauNet nodes

3. cs2.py - This is the implementation of CipherSaber-2 used to encrypt/decrypt messages

4. user_table.txt - This is the table of all TauNet nodes. It consists of user names followed by a | followed by either an IP address for the user or a domain name. Each user gets their own line. This table should be distributed to every node within your network.
Example:
user_name1|IP
user_name2|domain.com
user_name3|IP
.
.
.

5. data.txt - This holds your username, port info and other program data. It is laid out in the following format:
Line 1: your username
Line 2: port number - default 6283 according to TauNet protocol v0.2
Line 3: rounds of key scheduling - default 20 according to TauNet protocol v0.2
Line 4: version # - this release is 0.2
Line 5: max header size - default 90 explained below
Line 6: max message size - default 1KB according to TauNet protocol v0.2
Line 7: IV length used for encrypting messages. This is necessary to calculate total allowable input.

Note: This is how max header size is calculated in accordance with TauNet protocol v0.2
Header	Space	Payload	Line Ending	
8	1	3	2	
5	1	30	2	
3	1	30	2	
0	2	0	0	←--This is the space between header and main message
		Total Header	90	
		Total Input	934

--HOW TO OPERATE--
In order to recieve messages from other users do the following:
1. Open a terminal
2. Navigate to the folder locating the TN_Server.py
3. Type ./TN_Server.py into the command line and enter
4. Enter your encryption key for the session.
5. Wait for incoming messages.

In order to send messages to other users do the following:
1. Open a terminal
2. Navitgate to the folder locating the TN_Client.py
3. Type ./TN_Client.py into the command line and enter
4. Enter your encryption key for the session
5. Follow the prompts to send messages to otherTauNet users

Note: It is not necessary to have both applications open at the same time to operate either of them.

Note: If either program fails to open instead type python file_name.py
