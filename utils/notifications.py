import smtplib
from email.mime.text import MIMEText

def send_email(sender, password, receiver, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())

import pandas as pd

def check_overdue_tasks(df):
    today = pd.Timestamp.today()
    overdue = df[df["Data fine"] < today]
    return overdue

