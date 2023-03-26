import jwt
from mysite.settings import SECRET_KEY as KEY
from datetime import datetime,timedelta
from django.forms.models import model_to_dict 
import smtplib, ssl
from email.mime.text import MIMEText
from smtplib import  SMTPResponseException as SMTPExc
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError
from django.contrib import messages
import smtpd
from smtplib import SMTP

# smtp_server = 'mail.shop-recovery.net'
# login = "app@shop-recovery.net"
# password = "Shoprecovery_123"
# smtp = SMTP(host=smtp_server,port=587,)
# smtp.login(user=login,password=password)
# from_addr = 'app@shop-recovery.net'
# smtp.set_debuglevel(debuglevel=0)


def user_directory_path_QS_physicians(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'qs_physician/{0}_{1}/{2}'.format(instance.first_name,instance.last_name ,filename)

def verifyJWT(token,key=KEY):
    try:
        result = jwt.decode(key=key,jwt=token,algorithms=['HS256',],verify=True)
        print('result',result)
    except (InvalidSignatureError,ExpiredSignatureError) as ISE:
        print(ISE)
        print("xpppppppp")
        return False
    except (Exception) as DNE:
        print(DNE)
        print("xdddddddddd")
        return False
    else:
        return result
# Username:	app@shop-recovery.net
# Password:	Use the email account’s password.
# Incoming Server:	gator3270.hostgator.com
# IMAP Port: 993 POP3 Port: 995
# Outgoing Server:	gator3270.hostgator.com
# SMTP Port: 465

# smtp_server = 'mail.shop-recovery.net'
#     login = "app@shop-recovery.net"
#     password = "Shoprecovery_123"
#     smtp = SMTP(host=smtp_server,port=587,)
#     smtp.login(user=login,password=password)
#     from_addr = 'app@shop-recovery.net'
#     smtp.set_debuglevel(debuglevel=0)
def send_msg_email(message='This is a test message.',to='mahassan1456@gmail.com',previousURL=''):
    import smtplib
    
    from email.mime.multipart import MIMEMultipart 
    from email.mime.text import MIMEText
    server2 = 'gator3270.hostgator.com'
    server = 'mail.shop-recovery.net'
    app = 'app@shop-recovery.net'
    password = 'Shoprecovery_123'
    port = 587
    msg = MIMEMultipart()
    msg['From'] = 'app@shop-recovery.net'
    msg['To'] = to
    msg['Subject'] = 'Log In Credentials. '
    if '127' in previousURL or not previousURL:
        to="mahassan1456@gmail.com"
        message = "Development - TEST - " + message
   
    msg.attach(MIMEText(message))
    # to = 'whassan@shop-recovery.com'

  
    

    mailserver = smtplib.SMTP(server,port=port)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login(app, password=password)
    rcpt=['NOTIFY=SUCCESS,DELAY,FAILURE']   
    mailserver.sendmail(from_addr=app,to_addrs=to,msg=msg.as_string())

    mailserver.quit()

# def send(msg="This is a test email"):
#     smtp_server = 'mail.shop-recovery.net'
#     login = "app@shop-recovery.net"
#     password = "Shoprecovery_123"
#     smtp = SMTP(host=smtp_server,port=587,)
#     smtp.login(user=login,password=password)
#     from_addr = 'app@shop-recovery.net'
#     smtp.set_debuglevel(debuglevel=0)
  
#     to_addr = 'specialreminder@gmail.com'

#     try:
#         smtp.send_message(from_addr=from_addr,to_addrs=[to_addr],msg=msg)
#         # smtp.sendmail(from_addr, to_addr, msg,rcpt_options=['NOTIFY=SUCCESS,DELAY,FAILURE'])
#     except SMTPExc as error:
#         print(error)


# def send_msg_email(model='',message='Hello world how are you doing',to='whassan@shop-recovery.com'):
  
#     sender_email = 'app@shop-recovery.net'
#     smtp_server = 'mail.shop-recovery.net'
#     port = 465
#     login = "app@shop-recovery.net"
#     password = "Shoprecovery_123"
#     to_email = to
    
    

  
#     with smtplib.SMTP_SSL(smtp_server,port=port, context=context) as server:
#         server.login(sender_email, password)
#         server.sendmail(sender_email, to_email, message) 


def buildJWTGenericLink(model):

    # Generic Way to Build JWT for any model.

    payload = { (key[0:3] if len(key) > 2 else key):(value if isinstance(value,str) or isinstance(value,int) else f"id{model.id}-{datetime.now()}")   for key,value in model_to_dict(model).items() }
    payload['exp'] = datetime.now() + timedelta(days=1)
    
    # add the custom fields or changes which you want to implement

    payload['new'] = True if model.hospital_type == 'new' else False
    payload['onb'] = True if model.hospital_type == 'onboarded' else False
    payload['ivt'] = True if model.hospital_type == 'invite' else False

    # end of custom logic

    token = jwt.encode(payload=payload,key=KEY,algorithm=['HS256',])
   
    link = f'127.0.0.1/quickstart/token/validate/?token={token}'

    return link

def buildJWTQuickStartPhysician(qs_physician,domain='local',admin=True):
    print
    if not admin:
        token = jwt.encode(key=KEY,payload={
        "sid": qs_physician.id,
        "typ": 'onboarded',
        "eml": qs_physician.email,
        "cty": list(qs_physician.specialty.all().values_list('id','tag')),
        "nme": qs_physician.hospital_name,
        "new": False,
        "ety":"physician",
        "exp": datetime.now() + timedelta(days=1)
    },algorithm='HS256')
    else:
        print("stupid ass bitch")
        hospital_name = qs_physician.hospital_name
        if qs_physician.hospital_type == 'onboarded':
            hospital_name = qs_physician.hospital.name
        elif qs_physician.hospital_type == 'invite':
            hospital_name = qs_physician.hospital_invite.hospital_name
    
        token = jwt.encode(key=KEY,payload={
            "sid": qs_physician.id,
            "typ": qs_physician.hospital_type,
            "nme": hospital_name,
            "eml": qs_physician.email,
            "cty": list(qs_physician.specialty.all().values_list('id','tag')),
            "new": True,            
            "ety":"physician",
            "exp": datetime.now() + timedelta(days=31)
        },algorithm='HS256')
    print(domain)
    if domain == 'local' or '127' in domain:
        return f'127.0.0.1:8000/quickstart/token/validate/?token={token}&entity=physician',qs_physician.hospital_name
        
        
    return  f"http://44.213.1.13:8000/quickstart/token/validate/?token={token}&entity=physician",hospital_name

   

def buildJWTQuickStartHospital(qs_hospital,domain='local'):
    
    link = ''
    token = jwt.encode(key=KEY, payload= {
        "sid": qs_hospital.id,
        "nme":qs_hospital.hospital_name,
        "zip":qs_hospital.hospital_zip,
        "eml": qs_hospital.email,
        "phn":qs_hospital.phone,
        "fnm": qs_hospital.first_name,
        "lnm":qs_hospital.last_name,
        "ety": "hospital",
        "exp":datetime.now() + timedelta(days=1)
    }, algorithm='HS256')
    print('domain',domain)
    if domain == 'local' or '127' in domain:
        link = f'127.0.0.1:8000/quickstart/token/validate/?token={token}&entity=hospital'
        return link
    link = f"http://44.213.1.13:8000/quickstart/token/validate/?token={token}&entity=hospital"
    return link

# def createApprovalEmail(hospital,email='specialreminder@gmail.com'):
#     token = jwt.encode(key=KEY,payload={
#         "id": hospital.id,
#         "nme": hospital.name,
#         "exp": datetime.datetime.now() + datetime.timedelta(days=7)
#     },algorithm='HS256')

#     link = f'127.0.0.1:8000/medical/approvetoken/verify/?token={token}&hospital={hospital.id}'
#     html = get_template('login/createloginemail.html')
#     html = html.render({'hospital':hospital, 'link':link})
#     message = MIMEMultipart('alternative')
#     message["Subject"] = "Establish Login Credentials"
#     message["From"] = f"Acounts<accounts@randomthoughtz.com>"
#     message["To"] = email
#     text = f"""
#             Your hospital with the following details has been succesfully approved.
#             Name: {hospital.name}
#             Address: {hospital.street} {hospital.city} {hospital.state} {hospital.zip}
#             Total Physicians: {hospital.total_physicians}
#             Please visit the link below to create login credentials and began recommending products for participating physicians.
#             {link}
#             """
#     part1 = MIMEText(text, "plain")
#     part2 = MIMEText(html, "html")
#     message.attach(part1)
#     message.attach(part2)
#     context = ssl.create_default_context()

#     send_msg_email(message=message.as_string())


def buildAndSend(model='',type='',email='specialreminder@gmail.com'):

    if type == 'physician':
        link = buildJWTQuickStartPhysician(qs_physician=model)
    else:
        link = buildJWTQuickStartHospital(qs_hospital=model)
    
    
