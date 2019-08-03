import imaplib
import email
import os
import time

def check_mail():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('', '')
    mail.list()
    # Out: list of "folders" aka labels in gmail.
    mail.select("inbox") # connect to inbox.
    
    result, data = mail.uid('search', None, "ALL") # search and return uids instead
    latest_email_uid = data[0].split()[-1]
    result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = data[0][1] #.decode('utf-8')
    #including headers and alternate payloads
    email_message = email.message_from_bytes(raw_email)
    #print(email_message['To']
    
    if((email_message['Subject'].lower() == 'schedule') and ('anuj' in email.utils.parseaddr(email_message['From']))):
        os.system("")
    mail.close()



while(1):
    time.sleep(5)
    check_mail()


#print(email_message.items())# print all headers


##****************Alternate Code ***************************
##
##conn = imaplib.IMAP4_SSL('imap.gmail.com')
##
##try:
##    (retcode, capabilities) = conn.login('testbotforemail@gmail.com', '1mahandas1')
##except:
##    print(sys.exc_info()[1])
##    sys.exit(1)
##
##conn.select(readonly=1) # Select inbox or default namespace
##(retcode, messages) = conn.search(None, '(UNSEEN)')
##print(messages)
##if retcode == 'OK':
##    for num in messages[0].split(' '):
##        print('Processing :', message)
##        typ, data = conn.fetch(num,'(RFC822)')
##        msg = email.message_from_string(data[0][1])
##        typ, data = conn.store(num,'-FLAGS','\\Seen')
##        if ret == 'OK':
##            print(data,'\n',30*'-')
##            print(msg)
##
##conn.close()
