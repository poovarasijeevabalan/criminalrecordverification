from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from smtplib import SMTP
import smtplib, os
import sys
import datetime
import getpass

bot_id = getpass.getuser()
import json


def send_mail(config, dict_transaction):
    msg = MIMEMultipart()
    msg["Subject"] = "DDQC Report On (EST) " + str(datetime.datetime.now)
    # msg['Subject'] = dict_transaction['mail_subject']
    msg["From"] = config["mail_from"]
    msg["To"] = config["mail_to"]
    msg["CC"] = config["mail_cc"]
    to_email_id = msg["To"] + "," + msg["CC"]

    # message = dict_transaction["mail_message"]
    message = "DDQC Report On (EST) " + str(datetime.datetime.now)
    part1 = MIMEText(message, "plain")
    msg.attach(part1)

    server = smtplib.SMTP(config["mail_server"], config["mail_port"])
    server.starttls()
    # server.login(config["mail_from"], "Jvbln@618")
    server.sendmail(msg["From"], to_email_id.split(","), msg.as_string())
    server.quit()


if __name__ == "__main__":
    with open(
        r"C:\Users\mjeevaba\Documents\Python\DDQC\DDQC 2.0\Code\DDQC Rule Engine\config.json"
    ) as f:
        config = json.load(f)
    dict_transaction = {}
    dict_transaction["mail_subject"] = "ddqc_report"
    dict_transaction["mail_message"] = "test message"
    send_mail(config, dict_transaction)
