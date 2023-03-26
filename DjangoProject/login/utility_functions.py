import smtplib, ssl
from twilio.rest import Client
import os
from smtplib import  SMTPResponseException as SMTPExc
from twilio.base.exceptions import TwilioException, TwilioRestException 

AUTH_TOKEN = '010a7438fe4eb47acdb3cd55ec3b1116'
ACCOUNT_SID = 'AC69d437937a56eea0df43dfc62642d2ee'
MSG_SERV_SID = 'MGcaa37533bd0d8d597d654bbb3f95c24c'
from django.template.loader import get_template
from django.template import Context
import smtplib, ssl
from twilio.rest import Client
import os
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


PROD_AUTH_TOKEN = '72aad6924f45c7aa3345493d8b89c1f6'
PROD_ACCOUNT_SID = 'ACc66b454ce0b3939dd62d34ca1d87bd16'
MSG_SERV_SID = 'MGcaa37533bd0d8d597d654bbb3f95c24c'
TWILIO_PH = '+18337941921'



def send_msg_email(message, email=""):
    sender_email = 'accounts@randomthoughtz.com'
    smtp_server = 'mail.privateemail.com'
    port = 465
    login = "accounts@randomthoughtz.com"
    password = "Iverson01"
    to_email = email
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server,port=port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, to_email, message)
    except Exception as Err:
        print(Err,"Error")


def evaluate(value):
    if not value:
        return False
    return True

def send_sms(message='There has been a new facility added. Please check administrative console for more information'):
    account_sid = 'ACc66b454ce0b3939dd62d34ca1d87bd16'
    auth_token = '72aad6924f45c7aa3345493d8b89c1f6'
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(messaging_service_sid='MG2e3a4d637ff55af01b6afc86f848c653',body=message,to='+17134829222')
    except Exception as Err:
        print(Err)
        return False
    else:
        return True
    
def createHTML(title,link):

    with open('/Users/nefarioussmalls/Documents/Da Portfolio/Code/DjangoProject/login/templates/login/forgotpassword.html','r') as html:
        html_file = html.read()
        html_file = html_file.replace('{title}',title)
        html_file = html_file.replace('{link}', link)
        return html_file

# def createHTMLApproval(hospital=''):
#     with open('/Users/nefarioussmalls/Documents/Da Portfolio/Code/DjangoProject/login/templates/login/hospitalapprovalmsg.html') as html:
#         html_file = html.read()
#         html_file = html_file.replace()

    
def send_forgot_password(model,link='',approval=False):

    token = jwt.encode(key=KEY,payload={
        "id": model.id,
        "fir": model.first_name,
        "lst": model.last_name,
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=10)
    })
    if not link:
        link = f'/login/newpassword/?tmodeloken={token}&id={model.id}&hospital={model.hospital2.name}'
    result = True
    html = createHTML(model.get_full_name(), link=link)
    message = MIMEMultipart('alternative')
    message["Subject"] = "Reset Your Password for RandomThoughtz.Com"
    message["From"] = f"Accounts<accounts@randomthoughtz.com>"
    message["To"] = model.email
    text = f"""\
            Please copy and paste the following link in your browser \n
            {link}
            """
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()
    print("DOes It make it here????")
    send_msg_email(message=message.as_string())


def send_approve_hospital(hospital='',email="specialreminder@gmail.com", name='administrator',link='',approval=False):


    token1 = jwt.encode(key=KEY,payload={
        "id": hospital.id,
        "nme": hospital.name,
        "str": hospital.street,
        "sta": hospital.state,
        "cty": hospital.city,
        "zip": hospital.zip,
        "app": True,
        "exp": datetime.datetime.now() + datetime.timedelta(days=1)
    },algorithm='HS256')
    
    # link = f'/login/newpassword/?tmodeloken={token}&id={model.id}&hospital={model.hospital2.name}'
    link=''
    result = True
    subject = ''

    link_approve = f'127.0.0.1:8000/login/approval/admin/?app_code=True&token={token1}'
    html = get_template('login/hospitalapprovalmsg.html')
    html = html.render({'hospital':hospital,'name':name,'link_approve':link_approve})
    text = f"A hospital has been registered with the following details. Please log in to XXXXX.com to approve and view additional details. \
    Name:{hospital.name} \n Address: {hospital.street} {hospital.city} {hospital.state} {hospital.zip} \n Created Date/Time: {hospital.created_at}. \
        Submit Approval: {link_approve}"
    message = MIMEMultipart('alternative')
    message["subject"] = 'New Facility Added'
    message["from"] = "Accounts<accounts@randomthoughtz.com>"
    message["to"] = email
    part1 = MIMEText(text,'plain')
    part2 = MIMEText(html,'html')
    message.attach(part1)
    message.attach(part2)
    send_msg_email(message=message.as_string(),email=email)
    
    # html = createHTML(model.get_full_name(), link=link)
    # message = MIMEMultipart('alternative')
    # message["Subject"] = "Reset Your Password for RandomThoughtz.Com"
    # message["From"] = f"Accounts<accounts@randomthoughtz.com>"
    # message["To"] = model.email
    # text = f"""\
    #         Please copy and paste the following link in your browser \n
    #         {link}
    #         """
    # part1 = MIMEText(text, "plain")
    # part2 = MIMEText(html, "html")
    # message.attach(part1)
    # message.attach(part2)
    # context = ssl.create_default_context()
    # print("DOes It make it here????")
    # send_msg_email(message=message.as_string())

def user_profile_picture_directory_path(instance,filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'users/{0}_{1}/{2}'.format(instance.user.first_name,instance.user.last_name ,filename)



    