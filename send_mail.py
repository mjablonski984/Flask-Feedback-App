import os
import smtplib
from email.mime.text import MIMEText

def send_mail(name, email, source, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = os.environ.get('MAILTRAP_LOGIN')
    password = os.environ.get('MAILTRAP_PASSWORD')
    message = f"""<h3>New Feedback Submission</h3>
    <ul><li>Name: {name}</li>
    <li>Email:{email}</li>
    <li>Source: {source}</li>
    <li>Rating: {rating}</li>
    <li>Comments: {comments}</li></ul>
    """

    sender_email = email
    receiver_email = os.environ.get('RECEIVER_EMAIL')
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

     # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())