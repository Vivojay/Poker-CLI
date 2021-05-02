# Visit https://www.google.com/settings/security/lesssecureapps and "Turn ON"

#Easiest and Readable way to Email
#through Python SMTPLIB library
#This works with >>> Gmail.com <<<

import os
import smtplib
import json, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email.message import EmailMessage
from ascii_card_displayer import _dispCards

from unicards import unicard as uc


def SEND():
    with open('res/holes.json') as f:
        Hole_Cards = json.load(f)

    with open('res/emails.json') as f:
        Email_IDs = json.load(f)

    def CARD(*aas):
        return '&nbsp;'.join([uc(aa.replace('10', 'T')[0]+aa.replace('10', 'T')[1].lower()) for aa in aas])

    EmailAdd = os.environ['GMAIL_ID'] #senders Gmail id over here
    Pass = os.environ['GMAIL_PASS'] #senders Gmail's Password over here

    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(EmailAdd, Pass)

    for i, EID in zip( list(Hole_Cards.values()), Email_IDs ):
        msg = MIMEMultipart('alternative')

        EmailContent = CARD(*i)
        EmailContent = '''
        <html>
        
        <p style = "font-family: Courier New; font-size: 268px">
        '''+EmailContent+'''
        
        </p>
        </html>
        '''

        HTML = MIMEText(EmailContent, 'html')
        msg.attach(HTML)

        msg['Subject'] = 'Your poker hole cards'
        msg['From'] = EmailAdd
        msg['To'] = EID

        server.sendmail(EmailAdd, EID, msg.as_string())

    server.quit()
