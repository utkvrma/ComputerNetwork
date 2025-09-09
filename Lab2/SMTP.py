import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.ethereal.email"
SMTP_PORT = 587  
USERNAME = "samantha68@ethereal.email"
PASSWORD = "tx5jY9hb7VRPhq3kqs"

msg = MIMEMultipart()
msg["From"] = USERNAME
msg["To"] = "utkarshiitp27@gmail.com"
msg["Subject"] = "Hello from Python + Ethereal"

body = "This is a test email sent via smtplib and Ethereal from Samantha Rosenbaum!"
msg.attach(MIMEText(body, "plain"))

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls() 
    server.login(USERNAME, PASSWORD)

    server.sendmail(msg["From"], msg["To"], msg.as_string())
    print("Email sent successfully!")

    server.quit()
except Exception as e:
    print("Error:", e)
