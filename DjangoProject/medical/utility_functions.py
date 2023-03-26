import smtplib, ssl
from twilio.rest import Client
import os
from django.template.loader import get_template
from smtplib import  SMTPResponseException as SMTPExc
from twilio.base.exceptions import TwilioException, TwilioRestException
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
import jwt
from email.mime.text import MIMEText
from smtplib import  SMTPResponseException as SMTPExc

from twilio.base.exceptions import TwilioException, TwilioRestException
import datetime
from mysite.settings import SECRET_KEY as KEY, EMAIL_HOST as mail_server, EMAIL_HOST_USER as from_sender, EMAIL_HOST_PASSWORD as PWORD


AUTH_TOKEN = '010a7438fe4eb47acdb3cd55ec3b1116'
ACCOUNT_SID = 'AC69d437937a56eea0df43dfc62642d2ee'
MSG_SERV_SID = 'MGcaa37533bd0d8d597d654bbb3f95c24c'

def user_directory_path_hospital(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'register/{0}/{1}'.format(instance.name,filename)

def send_msg_email(model='',message='',to='specialreminder@gmail.com'):
    sender_email = 'accounts@randomthoughtz.com'
    smtp_server = 'mail.privateemail.com'
    port = 465
    login = "accounts@randomthoughtz.com"
    password = "Iverson01"
    to_email = to
    context = ssl.create_default_context()
  
    with smtplib.SMTP_SSL(smtp_server,port=port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, message)

def evaluate(value):
    if not value:
        return False
    return True

def send_sms(message='There has been a new facility added. Please check administrative console for more information'):
    AUTH_TOKEN = '010a7438fe4eb47acdb3cd55ec3b1116'
    auth_token = '010a7438fe4eb47acdb3cd55ec3b1116'
    account_sid = 'AC69d437937a56eea0df43dfc62642d2ee'
    
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        messaging_service_sid='MGcaa37533bd0d8d597d654bbb3f95c24c',
        body=message,
        to='+17134829222'
    )
def createHTML(title,link):

    with open('/Users/nefarioussmalls/Documents/Da Portfolio/Code/DjangoProject/login/templates/login/forgotpassword.html','r') as html:
        html_file = html.read()
        html_file = html_file.replace('{title}',title)
        html_file = html_file.replace('{link}', link)
        return html_file
    
def send_forgot_password(requested_user):

    token = jwt.encode(key=KEY,payload={
        "id": requested_user.id,
        "fir": requested_user.first_name,
        "lst": requested_user.last_name,
        "usr":requested_user.username,
        "eml":requested_user.email,
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=60)
    },algorithm='HS256')

    link = f'127.0.0.1/login/newpassword/?token={token}&uname={requested_user.username}&hospital={requested_user.hospital2.name}'
    html = createHTML(requested_user.get_full_name(), link=link)
    message = MIMEMultipart('alternative')
    message["Subject"] = "Reset Your Password for RandomThoughtz.Com"
    message["From"] = f"Accounts<accounts@randomthoughtz.com>"
    message["To"] = requested_user.email
    text = f"""\
            Please copy and paste the following link in your browser \n
            {link}
            """
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()

    send_msg_email(message=message.as_string())

def approveJWT():
    pass

def createApprovalEmail(hospital,email='specialreminder@gmail.com'):
    token = jwt.encode(key=KEY,payload={
        "id": hospital.id,
        "nme": hospital.name,
        "exp": datetime.datetime.now() + datetime.timedelta(days=7)
    },algorithm='HS256')

    link = f'127.0.0.1:8000/medical/approvetoken/verify/?token={token}&hospital={hospital.id}'
    html = get_template('login/createloginemail.html')
    html = html.render({'hospital':hospital, 'link':link})
    message = MIMEMultipart('alternative')
    message["Subject"] = "Establish Login Credentials"
    message["From"] = f"Acounts<accounts@randomthoughtz.com>"
    message["To"] = email
    text = f"""
            Your hospital with the following details has been succesfully approved.
            Name: {hospital.name}
            Address: {hospital.street} {hospital.city} {hospital.state} {hospital.zip}
            Total Physicians: {hospital.total_physicians}
            Please visit the link below to create login credentials and began recommending products for participating physicians.
            {link}
            """
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()

    send_msg_email(message=message.as_string())




    