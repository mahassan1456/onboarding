from django.shortcuts import render
from .forms import QuickStartPhysicianForm, QuickStartHospitalInvite
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from .utility_functions import buildJWTQuickStartPhysician,send_msg_email, verifyJWT
from smtplib import  SMTPResponseException as SMTPExc
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from mysite.settings import SECRET_KEY as key
from register.forms import AddHospital
from quickstart.utility_functions import send_msg_email as sme, buildJWTQuickStartHospital,buildJWTQuickStartPhysician
from .models import quickStartHospital1 as quickStartHospital, quickStartPhysician as qsp
from django.forms.models import model_to_dict
from django.contrib.auth.models import User 
from smtplib import  SMTPResponseException as SMTPExc
import smtplib, ssl
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from pproducts.models import ProductTags, Physician
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from medical.models import Hospital2
from support.models import ResidualData
import random
from smtplib import  SMTPResponseException as SMTPExc
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError
from .forms import quickStartPhysicianSimple,ImageForm
from .utility_functions import send_msg_email
from django.utils import timezone
from superuseractions.models import QuickInviteLogs,UserHistoryTable
from django.urls import reverse
from django.db import IntegrityError, DatabaseError, DataError
from support.utility_functions import returnExcelResponse
from superuseractions.models import UserHistoryTable

# def send_msg_email(model='',message='',to='specialreminder@gmail.com'):
#     sender_email = 'accounts@randomthoughtz.com'
#     smtp_server = 'mail.privateemail.com'
#     port = 465
#     login = "accounts@randomthoughtz.com"
#     password = "Iverson01"
#     to_email = to
#     context = ssl.create_default_context()
  
#     with smtplib.SMTP_SSL(smtp_server,port=port, context=context) as server:
#         server.login(sender_email, password)
#         server.sendmail(sender_email, to_email, message)
ERROR_MESSAGE = "There was an error processing your request.Please try again later."
@login_required
@user_passes_test(lambda u: u.is_superuser)
def assignAdmin(request,id):
    password = ''
    username = ''
    new_user = ''
    try:
        # Hospital is created first by a Manual Process.email has not been sent/login has not been created. 
        # AssignAdmin will create a username with the email used to send the credentials and a temporary password
        # which the user will be prompted to change upon loggin in for the first time.
        hospital = Hospital2.objects.get(id=id)
        print(hospital)
    except (Hospital2.DoesNotExist,Exception) as error:
        print(error)
        return
    # Hidden field in generated in the modal form and is set to True
    auto_create = request.POST.get('autocreate','')
    if auto_create:
        print("did it autocreate")
        email  = request.POST.get('email','')
        is_emailed = request.GET.get('isemailed','')
        username = email
        data = ResidualData.objects.first()
        random_int = random.randint(1,100)
        password = 'hospital' + str(data.user_number_track) + str(random_int)
        data.user_number_track += 1
        data.save()
        hospital.is_manual_time = timezone.now()

        # Build later to 

        # if not email:
        #     try:
        #         message = f"Please Log In with the credentials. Username: {hospital.email} and Password:{password}"
        #         send_msg_email(message=message, to=hospital.email,previousURL=request.META.get('HTTP_REFERER'))
        #     except SMTPExc as error:
        #         print(error)
        #         return HttpResponse("Error Processing Your Request.Please try again later.")
        #     except Exception as error:
        #         return HttpResponse("Error Processing Your Request.Please try again later.")
        #     else:
        #         messages.success(request=request,message=f"Succesfully sent a reminder to {hospital.email} at {hospital.name}")
        #         url = reverse('quickstart:assignAdmin') + ""
        #     return HttpResponseRedirect(redirect_to=url)

                


        print('autocreate')
        # if auto_create:
        #     # get form element
        #     username = email
        #     # grab running count for counting number of manual physicians and to ensure a random number.
        #     data = ResidualData.objects.first()
        #     random_int = random.randint(1,100)
        #     username = email
        #     password = 'hospital' + str(data.user_number_track) + str(random_int)
        #     data.user_number_track += 1
        #     data.save()

        #     print('username',username,'password',password)
        # else:
        #     # Pull data from prefilled information
        #     pass
        try:
            message = f"Your username is {username} and Password {password}"
            send_msg_email(message=message, to=email,previousURL=request.META.get('HTTP_REFERER'))
        except (SMTPExc,Exception) as error:
            print(error)
            messages.error(request,f"Invite can not be send. Please check is the email address is valid and try again.",extra_tags='warning')
            return HttpResponseRedirect(reverse('views:view_hospitals'))
        # for production
        # new_user = User.objects.create(username=email,email=email,prompt_credentials=True,hospitals=hospital)
        # Temp
        qsl = QuickInviteLogs(email=email,entity_name=hospital.name,entity_type="hospital",message=0,action="Manual Account Created")
        qsl.save()
        qsl.user = request.user
        qsl.save()
        hospital.is_emailed = True
        hospital.email = email
        hospital.is_manual_time = timezone.now()
       
    #  check why I amser  assigning hospital.u
        if hospital.user:
            if is_emailed:
                try:
                    existing_user  = hospital.user
                    existing_user.username = email
                    existing_user.email = email
                    existing_user.set_password(password)
                    existing_user.save()
                    hospital.save()
                except Exception as error:
                    print(error)
                    messages.error(request,message=f"Error processing your request.",extra_tags='warning')
                    return HttpResponseRedirect(reverse('views:view_hospitals'))
                messages.success(request,message=f"Sent Credentials to {email} at {hospital.name}",extra_tags='success')
                return HttpResponseRedirect(reverse('views:view_hospitals'))
        else:
            hospital.save()
            try:
                new_user = User.objects.create(username=username,email=email)
                # create log record
                uht = UserHistoryTable(action="1",entity_type="User",entity_name=email,entity_id=new_user.id,)
                uht.user = request.user
                uht.save()
                hospital.is_manual = True
                hospital.save()
                new_user.set_password(password)
                new_user.hospitals.add(hospital)
                new_user.userprofileadmin.prompt_credentials = True
                new_user.userprofileadmin.save()
                new_user.save()
            except Exception as error:
                print(error)
                messages.error(request=request,message=f"Error Processing Request.",extra_tags='warning')
                return HttpResponseRedirect(reverse('dashboard:master_dashboard'))
        

        messages.success(request,f"You have sent an invite to {new_user.username} with the username {new_user.username}",extra_tags='success')
        return HttpResponseRedirect(reverse('views:view_hospitals'))


    


def send_msg_email_quick(model='',message='',to='specialreminder@gmail.com'):
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

# Create your views here.

@login_required
def quickStartPhysicianStaff(request):
    if request.method == 'POST':
        form = quickStartPhysicianSimple(request.POST)
        if form.is_valid():
            qs_physician = form.save()
            qs_physician.is_assigned = True
            qs_physician.is_emailed = True
            qs_physician.hospital = request.user.hospitals.all()[0]
            qs_physician.save()
            link,hospital_name = buildJWTQuickStartPhysician(qs_physician=qs_physician,admin=False,domain=request.META.get('HTTP_HOST', ''))
            try:
                send_msg_email(message=f"Please click the following link to quick start physician {link}",to=qs_physician.email,previousURL=request.META.get('HTTP_REFERER'))
            except (SMTPExc,Exception) as error:
                print(error)
                return HttpResponse(f"{error}")
            qs_physician.is_emailed = True
            messages.success(request=request,message=f"Succesfully sent an invite to Physician: {qs_physician.first_name} {qs_physician.last_name} @ {qs_physician.email}",extra_tags='success')
            return render(request,template_name='quickstart/invite_physician_send_message.html',context={'qs_physician':qs_physician,'type':'physician','group':'staff'})

        
        messages.error(request,message="Please check the form for errors and try again",extra_tags='warning')
        return render(request,template_name='quickstart/invite_physician_.html',context={'form':form})

            
        
    form = quickStartPhysicianSimple()
    return render(request,template_name='quickstart/invite_physician_.html',context={'form':form})

# Displaying the form to the SuperUser to QuickStart a Physician
@login_required
@user_passes_test(lambda u: u.is_superuser)
def quickStartPhysician(request):
    
    header = "Quick Start Physician"
    invite = "Send Invite"
    send_to_admin = False
    if request.method == 'POST':

       
        print(quickStartHospital.objects.all())

        form = QuickStartPhysicianForm(data = request.POST)
        if form.is_valid():
            hospital_type = form.cleaned_data.get('hospital_type','')
            email_options = form.cleaned_data.get('email_options','')
            try:
                qs_physician = form.save(commit=True)
            except Exception as error:
                messages.error("Ooops! There was an error Sending the Invite. Please contact the administrator or try again later.",extra_tags='warning')
                return HttpResponseRedirect(reverse('views:quickStartPhysician')) 
            
            # craft JWT Link to send
            try:
                # build the jwt link and check my host to determine what link to create the link for.
                link,hospital_name = buildJWTQuickStartPhysician(qs_physician=qs_physician,domain=request.META.get('HTTP_HOST', ''),admin=True)
                email = qs_physician.email
                # Write a Custom Email if email_options == 1 else 
                if email_options == 1:
                    message= f"{form.cleaned_data.get('email_message','')}. Please click the following secure link to begin recommending products. \n {link}"
                else:
                    message = f"Hello Physician {qs_physician.first_name} {qs_physician.last_name}. Please copy and paste the following secure link in your browser to quickstart. {link}"
                send_msg_email(message=message,previousURL=request.META.get('HTTP_REFERER'),to=qs_physician.email)
            except (SMTPExc) as smtp:
                messages.error(request=request,message=f"There was an error sending an invite email to {qs_physician.first_name} {qs_physician.last_name}",extra_tags='warning')
                return HttpResponse(content=ERROR_MESSAGE)
            except (Exception) as error:
                messages.error(request=request,message=f"An exception occurred while processing your request. Please try again or contact the administrator if the problem persists.",extra_tags='warning')
                return HttpResponse(ERROR_MESSAGE)
            # Create A log record of the email being sent.
            else:
                qsl = qs_physician.logRecord(email_options=email_options,user=request.user)
                # qsl = QuickInviteLogs(email=email,entity_name=qs_physician.getHospitalName(),entity_type="physician",message=int(email_options),action="Quick Invite(Physician)")
                # qsl.user = request.user
                # qsl.save()
                qs_physician.is_emailed = True
                qs_physician.setState()
            # If dont assign is selected then our work here is done. We have saved the record to the database.
            if hospital_type == "na":
                messages.success(request,f"Succesfully added physician {qs_physician.get_full_name()}. Please Note: This physician is currently not assigned to any hospital.",extra_tags='success')
                return HttpResponseRedirect(reverse('dashboard:master_dashboard'))

            # for new hospital added steps to create a quick start entity and associating it with the  physician included the form.
            if hospital_type == 'new':

                hospital_name = form.cleaned_data.get('hospital_name','').strip()
                hospital_email = form.cleaned_data.get('hospital_email','').strip()
                # If new hospital is created qs_physician automatically becomes assigned.
                if hospital_email:
                    try:
                        qs_hospital = quickStartHospital.objects.create(hospital_name=hospital_name,email=hospital_email)
                        qs_physician.is_assigned = True
                        link = buildJWTQuickStartHospital(qs_hospital=qs_hospital,domain=request.META.get('HTTP_HOST', ''))
                        message = f"Hello admin for {qs_hospital.hospital_name} Please copy and paste the following secure link in your browser to quickstart. {link}"
                        send_msg_email(message=message,to='specialreminder@gmail.com')
                        send_to_admin = True
                    except (SMTPExc,Exception) as error:
                        print(error)
                        return HttpResponse(ERROR_MESSAGE)
                    qs_hospital.is_emailed = True
                    qs_hospital.qs_physicians.add(qs_physician)
                    qs_hospital.save()
                    try:
                        qsl = QuickInviteLogs(email=hospital_email,entity_type="hospital",entity_name=hospital_name,message=int(email_options),action="Quick Invite(Hospital)")
                        qsl.user = request.user
                        qsl.save()
                    except IntegrityError as error:
                        messages.error(request,message=f"There was an error processing your request. Please conact the administrator or try again later.")
                    except DataError as error:
                        messages.error(request,message=f"There was an error processing your request. Please conact the administrator or try again later.")
                    except DatabaseError as error:
                        messages.error(request,message=f"There was an error processing your request. Please conact the administrator or try again later.")

                else:
                    return ValidationError(message="When sending a physician invite with a New Hospital a valid email address must be associated with the Hospital. ")
                
            # elif hospital_type == 'na':
            if send_to_admin:
                messages.success(request=request,message=f"Your Physician Invite was Sent Succesfully.")
            else:
                messages.success(request=request,message=f"Your Physician Invite was Sent Succesfully.")
            QuickInviteLogs()
            return render(request,template_name='quickstart/invite_physician_send_message.html',context={'qs_physician':qs_physician,'type':'physician','group':'superuser'})
        print(form.errors)
        return render(request=request, template_name='quickstart/qs_physician.html', context={'form':form,'header':header,'button':invite})

    form = QuickStartPhysicianForm()
    return render(request=request, template_name='quickstart/qs_physician.html', context={'form':form,'header':header,'button':invite})


#Displaying the form to a SuperUser for quickstarting a Hospital.
def quickStartHosital(request):

    if request.method == 'POST':
        print(request.POST)
        form = QuickStartHospitalInvite(request.POST)
        if form.is_valid():
            qs_hospital = form.save()
            try:
                link = buildJWTQuickStartHospital(qs_hospital=qs_hospital,domain=request.META.get('HTTP_HOST', ''))
                message = f"Thank You for Signing Up. Please visit the secure link to quick start hospital. {link}"
                send_msg_email_quick(message=message)
            except (SMTPExc) as smtp:
                messages.error(request=request,message=f"There was an error sending an invite email to {qs_hospital.hospital_name}.",extra_tags='warning')
                return HttpResponse(f"{smtp}")
            except (Exception) as error:
                messages.error(request=request,message=f"An exception occurred while processing your request. Please try again or contact the administrator if the problem persists.",extra_tags='warning')
                return HttpResponse(f"{error}")
            try:
                qsl = QuickInviteLogs(email=qs_hospital.email,entity_type="hospital",entity_name=qs_hospital.hospital_name,message=0)
                qsl.user = request.user
                qsl.save()
            except Exception as error:
                messages.error(request,message=f"Error Processing Request",extra_tags='warning')
            else:
                messages.success(request=request,message=f"Succesfully sent an invite to Name: {qs_hospital.hospital_name} @ Email: {qs_hospital.email}",extra_tags='success')
            return HttpResponseRedirect(reverse('medical:dashboard'))

        
        return render(request,template_name='quickstart/quickStartHospital.html', context={'form':form})
            
    form = QuickStartHospitalInvite()
    return render(request,template_name='quickstart/quickStartHospital.html', context={'form':form})


def invitedHospital(request,id):
    try:
        qs_hospital = quickStartHospital.objects.get(id=id)
    except (quickStartHospital.DoesNotExist,Exception) as error:
        print(error)
        return HttpResponse(content="There was an error submitting your request. Please contact the administrator if the problem persists.")
    if request.method == 'POST':
       
        form = AddHospital(request.POST,request.FILES)
        if form.is_valid():
            
            onboarded_hospital = form.save()
            qs_hospital.is_registered = True
            phy_set = qs_hospital.qs_physicians.filter(is_recommending=True)

            print('phy_set',phy_set)
            if phy_set:
                physician_holder = []
                for phys in phy_set:

                    data = phys.convertToOnboarded()
                    
                    tags = phys.specialty.all()
                    physician=Physician.objects.create(**data)
                    physician.specialty_ph.add(*phys.specialty.all())
                    physician.buildLPT()
                    phys.is_onboarded = True
                    phys.save()
                    physician_holder.append(physician)
                    hospital_identifier_name = f"({physician.facility.name})" if physician.facility else ''
                    uht = UserHistoryTable.objects.create(action='4',entity_type='Physician',entity_name=f"{physician.get_full_name()}{hospital_identifier_name}",entity_id=physician.id,page_link=f"/views/physician/detail/{physician.id}/",action_verbose=" New Physician ")
                    uht.save()

                onboarded_hospital.physician_set.add(*physician_holder)
                onboarded_hospital.has_physicians = True
            # qs_hospital.save()
            # 
            admin = User.objects.create(email=qs_hospital.email,username=qs_hospital.email,first_name=qs_hospital.first_name,last_name=qs_hospital.last_name)
            admin.qs_hospital = qs_hospital
            admin.hospitals.add(onboarded_hospital)
            admin.userprofileadmin.mobile_contact = qs_hospital.phone
            admin.save()
            admin.userprofileadmin.save()
            qs_hospital.save()
            onboarded_hospital.save()
            onboarded_hospital.logRecord(action="1",action_verbose = " Account for ")

            # Write the function for converting from
            # qs_hospital.onboardPhysicians()

            return render(request=request,template_name='register/account_created.html',context={'admin':admin})
        
        return render(request,template_name='register/registration_quick_start.html',context={'form':form,'qs_hosp':qs_hospital})
    # fields = [key for key,value in mdel_to_dict(qs_hospital).items() if not value ]
    form = AddHospital(initial = {'name':qs_hospital.hospital_name,'email':qs_hospital.email,'zip':qs_hospital.hospital_zip})
    return render(request,template_name='register/registration_quick_start.html',context={'form':form,'qs_hosp':qs_hospital})

# def quickP(request):
#     return render
def validateToken(request):
    # Get the query parameters which is the token and the entity type of either physician or hospital
    import jwt
    token = request.GET.get('token','')
    entity = request.GET.get('entity','')
    json_token = verifyJWT(token=token,key=key)
    # Validate token received when User Clicks Link
    if json_token:
        # Do Something with the logic and build the web page.
        """if the token is valid check the entity type. Dependent upon the type of entity the user will be redirected to a specific
         page """
        object_id = json_token.get("sid","")
        if entity == 'hospital':
            try:
                qs_hospital = quickStartHospital.objects.get(id=object_id)
            except (quickStartHospital.DoesNotExist, Exception) as error:
                print(error)
                return HttpResponse(content=f"This is an error message. Error----{error}-----Error.")
            else:
                # build the URL and include the quick invited hospital in the query string
                url = reverse('quickstart:invitedHospital', args=(qs_hospital.id,))
                return HttpResponseRedirect(redirect_to=url)
        else:
            try:
                qs_physician = qsp.objects.get(id=object_id)
            except (qsp.DoesNotExist, Exception) as error:
                return HttpResponse(f"{error}")
            else:
                url = reverse('quickstart:invitedPhysician', args=(qs_physician.id,))
                return HttpResponseRedirect(redirect_to=url)
    else:
        return HttpResponse(content=f"Expired token-{token}. Please contact the administrator if you feel you have received this message in error. ")
    
def invitedPhysician(request,id):
    # Quickstart physician is created upon sending email so it is required to retrieve the record before proceeding.
    form = ImageForm()
    url = ''
    selections = ''
    existing_physician = ''
    onboarded_physician = ''
    onboarded = True
    try:
        qs_physician = qsp.objects.get(id=id) 
    except (qsp.DoesNotExist, Exception) as error:
        return HttpResponse(f"{error}")
    # Order tags to provide physician specialty choices.
    tags = ProductTags.objects.all().order_by('tag')
    if request.method == "POST":
        selections = request.POST.get('selections','')
        if not selections:
            messages.error(request="It is required that you select at least one specialty before recommending any products. If you select a specialty without selecting any corresponing products then all the products under the corresponding specialty will be selected to recommend.",extra_tags='warning')
        else:
            form = ImageForm(files=request.FILES)
            about_me = request.POST.get('about_physician','')
            # Make sure to test later if specialty is selected but an empty string is given
            products = qs_physician.buildProductsQuick(data=request.POST)
            qs_physician.is_recommending = True
            form.is_valid()
            qs_physician.picture = form.cleaned_data.get('image','')
            qs_physician.about_me = about_me
        
            if qs_physician.hospital:
                
                try:
                    existing_physician = Physician.objects.filter(firstName=qs_physician.first_name,lastName=qs_physician.last_name,email=qs_physician.email )
                    if existing_physician:
                        messages.error(request,message="You have already registered and are currently recommending products. Please contact your administrator to make further changes to your products or specialties.",extra_tags='warning')
                        return render(request,template_name='quickstart/welcome_physician.html',context={'tags':tags,'qs_physician':qs_physician,'form':form})

                except Exception as error:
                    print(error)
                    messages.error(request,message="There was an error processing your request. Please contact the administrator for more details.",extra_tags='warning')
                    return render(request,template_name='quickstart/welcome_physician.html',context={'tags':tags,'qs_physician':qs_physician,'form':form})

                # Build a new physician
                try:
                    specialty_ph = qs_physician.specialty.all()
                    data = {
                        'firstName': qs_physician.first_name,
                        'lastName':qs_physician.last_name,
                        'picture':form.cleaned_data.get('image',''),
                        'description': qs_physician.description,
                        'email': qs_physician.email,
                        'products':qs_physician.products,
                        'about_me':about_me
                    }
                    onboarded_physician = Physician.objects.create(**data)
                    onboarded_physician.specialty_ph.add(*specialty_ph)
                    onboarded_hospital = qs_physician.hospital
                    onboarded_hospital.physician_set.add(onboarded_physician)
                    onboarded_hospital.has_physicians = True
                    onboarded_hospital.save()

                except (ValidationError,IntegrityError) as error:
                    return HttpResponse(f"{error}")
                
                qs_physician.is_onboarded = True
                qs_physician.save()
                onboarded_physician.buildLPT()
                onboarded_physician.save()
                onboarded = True
                user = User.objects.get(username="anonymous")
                
                if onboarded:
                    uht = UserHistoryTable.objects.create(action='4',entity_type='Physician',entity_name=f"{onboarded_physician.get_full_name()}({onboarded_physician.facility.name.title()})",entity_id=onboarded_physician.id,page_link=f"/views/physician/detail/{onboarded_physician.id}/",action_verbose=" New Physician ")
                else:
                    
                    uht = UserHistoryTable.objects.create(action='5',entity_type='Physician(QS/Invite)', entity_name=f"{qs_physician.get_full_name()}({qs_physician.getHospitalName()})", entity_id=qs_physician.id,page_link=f"/views/physician/detail/{qs_physician.id}/",action_verbose=f" is recommending products for the specialties {qs_physician.buildSpecialtyString()}.")

                uht.user = user
                uht.save()

            # if physician is not onboarding to an already onboarded hospital nothing needs to be done besides potentially saving the picture and adding products and specialties as well as a BIO
            # messages.success(request=request,message=f"Thank You {qs_physician.get_full_name()} for completing registration. Here is a summary of your current specialties and products which you are recommending. {qs_physician.buildProductsString}. Please contact your administrator for further details on updating your specialties or recommended products. ",extra_tags='success')
            # uht = UserHistoryTable(action='1',entity_type='Physician',entity_name=qs_physician.get_full_name(),entity_id)
            return HttpResponseRedirect(reverse('quickstart:thank_you',args=(qs_physician.id,)))
    
        
    return render(request,template_name='quickstart/welcome_physician.html',context={'tags':tags,'qs_physician':qs_physician,'form':form})



def thinkYou(request,id):
    import pandas as pd
    
    welcome = ''
    try:
        qs_physician = qsp.objects.get(id=id)
        print('qs_physician',qs_physician)
    except qsp.DoesNotExist as error:
        print(error)
        messages.error(request,message=f"There was an error Processing your request. Please contact the administrator or try again later.")
    else:
        welcome = True
        download = request.GET.get('download','')
        print('download',download)
        if download:

            qs_physician_d = {

                'id':qs_physician.id,
                'full_name':qs_physician.get_full_name(),
                'email':qs_physician.email,
                'description':qs_physician.description,
                'specialty': qs_physician.buildSpecialtyString(),
                'products':qs_physician.products,
                'created_at': qs_physician.returnCreatedAt()
            }

            dataframe = pd.DataFrame(qs_physician_d)
            print(dataframe,'dataframe')

            sheet = "sheet"
            file_name = "physiciansummary.xlsx"

            return returnExcelResponse(dataframe=dataframe,sheet=sheet,file_name=file_name)

    return render(request,template_name='register/invite_hospital_send_message.html',context={'welcome':welcome,'qs_physician':qs_physician})

def buildProducts(request):

    specialty = request.POST.getlist('lookup','')[0].strip().title()
    specialty_products = ProductTags.objects.filter(tag=specialty)[0].products.all().order_by('name')
    products1 = [[product.name,product.getFirstImage(),product.description,product.id] for product in specialty_products ]
    products = list(ProductTags.objects.filter(tag=specialty)[0].products.all().order_by('name').values_list('name','picture','short_description','id'))
    print(products1)
    return JsonResponse(data={'dataset':products1,'specialty':specialty})

