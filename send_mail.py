import smtplib
import ssl
import subprocess
import schedule
import time
from datetime import datetime

from thing import daily_digest, all_tables, today
from parse_doc import process_data

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def get_email_message(sender_email, receiver_email):

    message = MIMEMultipart("alternative")
    message["Subject"] = daily_digest()
    message["From"] = sender_email
    message["To"] = receiver_email

    file1 = open("data.md", "w")
    file1.write(all_tables())
    file1.close()

    filename = "data.md"

    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    message.attach(part)

    body = "bot by yours truly Luke Yeh"
    message.attach(MIMEText(body, "plain"))

    return message.as_string()


def send_mail():
    print("sending")
    rc = subprocess.call("./download.sh", shell=True)
    process_data(today() + ".docx", save=True)

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
