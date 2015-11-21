#holds a message formatted according to the TauNet protocol
class Message():
   def __init__(self):
      self.version = 'Undefined'
      self.sender = 'Undefined'
      self.reciever = 'Undefined'
      self.message = 'Undefined'

   #takes a message recieved using the TauNet protocol and splits
   #it into its components and formats them for output to the screen.
   #variables:
   #message: should be decrypted already
   def set_message(self, message):
      message = message.rstrip()
      message = message.rsplit('\n')
      self.version = message[0]
      self.sender = message[1]
      self.reciever = message[2]
      self.message = '\n' + message[4]
   
   def display(self):
      print self.version
      print self.sender
      print self.reciever
      print self.message

   def edit(self, string):
      string = 'ball shot'

def main():
   message = Message()
   #string = 'version: ' + version + '\nfrom: ' sender + '\nto: ' + reciever + '\n\na message'
   #message.set_message(string)
   #message.display()
   string = 'cats eat'
   print string
   message.edit(string)
   print string
main()
