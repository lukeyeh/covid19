import smtplib
import ssl
import subprocess
import schedule
import time
import re
import requests

from datetime import datetime
from bs4 import BeautifulSoup
from get_data import find_cases

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def crawl():
    req = requests.get("https://www.amherstma.gov/3519/")
    soup = BeautifulSoup(req.text, "html.parser")
    return soup


def get_email_message(sender_email, receiver_email):

    message = MIMEMultipart("alternative")

    message["Subject"] = str(find_cases(crawl())) 
    message["From"] = sender_email
    message["To"] = receiver_email

    body = "bot by yours truly Luke Yeh"
    message.attach(MIMEText(body, "plain"))

    return message.as_string()


def send_mail():
    port = 465 

    context = ssl.create_default_context()
    password = open('password.txt', 'r').read().splitlines()[0]  

    sender_email = "covid19digestmass@gmail.com"
    receiver_emails = open("email_list.txt", 'r').read().splitlines()

    for receiver_email in receiver_emails:

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email,
                            get_email_message(sender_email, receiver_email))


if __name__ == '__main__':

    schedule.every().day.at("16:05").do(send_mail)
    while 1:
        schedule.run_pending()
        time.sleep(1)
