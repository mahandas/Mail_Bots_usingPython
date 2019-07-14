#!/usr/bin/env python
# encoding: utf-8
"""
python_3_email_with_attachment.py
Created by Robert Dempsey on 12/6/14.
Copyright (c) 2014 Robert Dempsey. Use at your own peril.
This script works with Python 3.x
NOTE: replace values in ALL CAPS with your own values
"""
import sys
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


#img_attachment = 'C:/Users/mahan.das/AppData/Local/Programs/Python/Python36/bob.jpg'
fname ='D:/Cbackup/Users/mahan.das/AppData/Local/Programs/Python/Python36/QuotesForTheDay.txt'
with open(fname) as f:
    content = f.readlines()
content = [x.strip() for x in content]
file_count_location='D:/Cbackup/Users/mahan.das/AppData/Local/Programs/Python/Python36/Count.txt'
file_count = open(file_count_location,encoding='utf-8')
Count = file_count.read()
file_count.close()
today = str(datetime.datetime.now().date())
COMMASPACE = ', '
text = "This is an automated python mail with a HTML Page attached to it and also a new Quote of the day. Below is the summary of a play by Shakespeare."
file1 = open('D:/Cbackup/Users/mahan.das/Desktop/HtmlFormail.txt',encoding='utf-8', errors='ignore')
html = file1.read()

def main():
    sender = 'mahan.d@finiq.com'
    gmail_password = '1mahandas1'
    #'namrata.bamb@finiq.com','bhumika.j@finiq.com','deepa.kulkarni@finiq.com','sarvanan.g@finiq.com','chandrakanth.e@finiq.com','yeshwanth.b.s@finiq.com','anuj.c@finiq.com','neelay.k@finiq.com',
    recipients = ['namrata.bamb@finiq.com','bhumika.j@finiq.com','deepa.kulkarni@finiq.com','priyanka.s@finiq.com','chandrakanth.e@finiq.com','saurabh.n@finiq.com','anuj.c@finiq.com','pooja.singh@finiq.com','mahan.d@finiq.com','sanket.m@finiq.com','dipak.g@finiq.com']
    
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = content[int(Count)]
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # List of attachments
    attachments = ['D:/Cbackup/Users/mahan.das/Desktop/text2CSV.txt']

    # Add the attachments to the message
    for file in attachments:
        try:
            outer.attach(MIMEText(text, 'plain'))
            outer.attach(MIMEText(html, 'html'))
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            #outer.attach(msg)
            if(os.path.isfile(file_count_location)):
                os.remove(file_count_location)
            new_count = open(file_count_location,'w')
            new_count.write(str(int(Count) + 2))
            new_count.close()
            #fp_1 = open(img_attachment, 'rb')                                                    
            #img1 = MIMEImage(fp_1.read())
            #fp_1.close()
            #img1.add_header('Content-ID', '<{}>'.format(img_attachment))
            #outer.attach(img1)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise

if __name__ == '__main__':
    main()
