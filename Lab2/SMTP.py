import smtplib
from email.mime.text import MIMEText

def send_email():
    sender = "hello@demomailtrap.co"
    receiver = "utkarshiitp27@gmail.com"
    username = "api"
    password = "password"   

    msg = MIMEText("Hello Utkarsh, I am Mailtrap.")
    msg["Subject"] = "CN Lab 2 - Test"
    msg["From"] = sender
    msg["To"] = receiver

    try:
        s = smtplib.SMTP("live.smtp.mailtrap.io", 587)
        s.starttls()
        s.login(username, password)
        s.sendmail(sender, receiver, msg.as_string())
        s.quit()
        print("Email sent successfully.")
    except Exception as e:
        print("Error:", e)

send_email()
