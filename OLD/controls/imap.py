import imaplib

username = '' 
password = '' 
mailbox = 'INBOX' 

mailserver = 'imap.gmail.com'
port = 993

server = imaplib.IMAP4_SSL(mailserver,port)
server.login(username,password)
server.select(mailbox)
data = str(server.status(mailbox, '(MESSAGES UNSEEN)'))
print
tokens = data.split()

print "you have ",
print tokens[5].replace(')\'])',''), tokens[4],
print " mails"
print
server.close()

server.logout()

