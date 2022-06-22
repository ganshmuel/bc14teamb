import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#server.login('gansmueltests@gmail.com','ufnfsjzdytbjnugz')

gmail_user = 'gansmueltests@gmail.com'
gmail_password = 'ufnfsjzdytbjnugz'

sent_from = gmail_user
to = ['gansmueltests@gmail.com', 'guybrylov@gmail.com']
subject = 'OMG Super Important Message'
body = 'Hey, what\'s up?\n\n- You'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print('Email sent!')
except:
    print('Something went wrong...')