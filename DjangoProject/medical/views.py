from django.shortcuts import render,redirect
from medical.forms import AddHospital, CredentialsForm, ContactForm, Login,CredentialsFormAdmin
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.forms.models import model_to_dict 
import re
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError
import jwt
from django.contrib.auth.decorators import user_passes_test
from medical.models import  Hospital2 as Hospital
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout as logout_user
from django.contrib.auth import login as login_user
from django.contrib.auth.models import User
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.utils import timezone
from medical.utility_functions import send_msg_email, evaluate, send_sms, createApprovalEmail
# Create your views here.
from smtplib import  SMTPResponseException as SMTPExc
import time
from twilio.base.exceptions import TwilioException, TwilioRestException
import logging
from login.models import WaitingRoom
from mysite.settings import SECRET_KEY as KEY

logger = logging.getLogger(__name__)

def login(request):
    header = "Welcome Back"
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('medical:dashboard'))

    if request.method == 'POST':

        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username','').lower()
            password = form.cleaned_data.get('password','')

            user = authenticate(request,username=username,password=password)
            url = request.GET.get('next', '')
            
            if user is not None:
                login_user(request, user)
                return HttpResponseRedirect(url if url else reverse('medical:dashboard'))
            else:
                messages.error(request, "Username or Password is Incorrect", extra_tags='code')
            
            return render(request,'medical/login1.html', context={'form':form,'button':'login'})

    user = False
    form = Login()
    return render(request, 'medical/login1.html',context={'form': form,'header':header,'button':'login'})

def login1(request):

    if request.method == 'POST':
        
        username = request.POST['username'].lower()
        password = request.POST['password']
    
        if not evaluate(username) or not evaluate(password):
            messages.error(request,message="Please provide login credentials",extra_tags='code')
            return HttpResponseRedirect(reverse('medical:login'))

        user = authenticate(request,username=username,password=password)
        url = request.GET.get('next', '')

        if user is not None:
            login_user(request, user)
            return HttpResponseRedirect(url if url else reverse('medical:dashboard'))
        else:
            messages.error(request, "Username or Password is Incorrect", extra_tags='code')
            return HttpResponseRedirect(reverse('medical:login'))

    user = False
    header = "Welcome Back"
    form = Login()
    return render(request, 'medical/login1.html',context={'form': form,'header':header})

def logout(request):

    logout_user(request)
    return HttpResponseRedirect(reverse('medical:login'))

@login_required
def addfacility(request):

    pass

@login_required
def success(request):
    
    return render(request=request, template_name="medical/blank.html",context={'head':'testifworks','vb': 'seeifiwork'})

def register(request, id=None):
    
    header = "Add Facility"
    button = "Create New Facility"
    print("fuckkfefjkrbferjbfklpppp")
    if request.method == 'POST':
        form = AddHospital(request.POST)
        
        if form.is_valid():
            hospital = form.save(commit=True)
            hospital.logHistory(user=request.user.username,created=True)



            if request.user.is_authenticated:
                if request.user.is_superuser:
                    hospital.approved_by = request.user.username
                    hospital.approved_at = timezone.now()
                    hospital.approved = True
                    hospital.save_no_history()

                messages.success(request, f"Sucessfully Added Hospital {hospital.name}")
                return HttpResponseRedirect(reverse('medical:dashboard'))

            # messages.success(request, "HOSPITAL ADDED SUCCESFULLY. PLEASE CREATE LOG IN CREDENTIALS", extra_tags='code')
            # return HttpResponseRedirect(reverse('medical:createuser', args=(hospital.id,) ))
        print("fuck u")
        print(form.errors)
        return render(request, 'medical/contactus1.html', context={'form':form,'header':header,'button':button})

            
    form = AddHospital()
    
    return render(request, 'medical/contactus1.html', context={'form':form,'header':header, 'button_text': 'Add Facility'})

def register1(request, id=None):
    
    header = "Add Facility"
    button = "Create New Facility"
    if request.method == 'POST':
        form = AddHospital(request.POST)
        
        if form.is_valid():
            hospital = form.save(commit=True)
        
            if request.user.is_authenticated:
                messages.success(request, f"Sucessfully Added Hospital {hospital.name}.")
                return HttpResponseRedirect(reverse('medical:dashboard'))

            messages.success(request, f"A request has been sent to the administrator for approval. Once approval has been confirmed an email will be sent containing a link to establish log in credentials")
            message = f"A hospital has been registered with the following details Name: {hospital.name} Address: {hospital.street} {hospital.city}, {hospital.state} {hospital.zip} @ {hospital.created_at}"
            return HttpResponseRedirect(reverse('medical:createuser', args=(hospital.id,) ))
        
        return render(request, 'medical/contactus1.html', context={'form':form,'header':header,'button':button})

            
    form = AddHospital()
    
    return render(request, 'medical/contactus1.html', context={'form':form,'header':header, 'button_text': 'Add Facility'})

@login_required
def dashboard(request):

    if not request.user.userprofileadmin.mobile_contact and not request.user.is_superuser:
        messages.warning(request, message="Please update your Mobile Contact Information in the Profile Section")
    
    
    return render(request=request, template_name='medical/dashboard.html')

def createuser(request, hospital_id = 0):

    print('hereeeee')
    header=''
    button_text = ''
    if hospital_id == 999:
        if request.method == 'POST':
            form = CredentialsFormAdmin(request.POST)
            if form.is_valid():
                form.save(commit=True)
                return HttpResponseRedirect(reverse('medical:dashboard'))
            return render(request=request, template_name='medical/contactus1.html', context={'form': form,'header':header,'button_text': button_text})
        header = 'Create Hospital Administrator'
        button_text = 'Create User'
        form = CredentialsFormAdmin()
        return render(request=request, template_name='medical/contactus1.html', context={'form': form,'header':header,'button_text': button_text})

    header = "Create Log In Credentials"
    button_text = 'Create User'
    if request.method == "POST":
        bound_form = CredentialsForm(request.POST)

        if bound_form.is_valid() and hospital_id:
            print()
            clearTextPassWord = request.POST.get('password1')
            print(clearTextPassWord)
            try:
                hospital = Hospital.objects.get(id = hospital_id)
            except Hospital.DoesNotExist as hdne:
                messages.error(request,message="AN Error Occcured while processing  your request. Please try again later")
                #Log Error
                return HttpResponseRedirect(reverse('medical:contactus'))
            else:
                try:
                    new_user = bound_form.save(commit=True)
                    hospital.user = new_user
                    hospital.save()
                except Exception as exp:
                    messages.error(request, message='There was an error processing your request. Please check data for valid input and try again. If the problem persists please contact the administrator by visiting Contact Us')
                    return HttpResponseRedirect(reverse('medical:contactus'))
                else:
                    if request.user.is_superuser:
                        messages.success(request,message=f"Succesfully created new user {new_user.get_full_name()} for Hospital {hospital.name}")
                        try:
                            # Add Email when email function is working to send email to other users
                            # send_msg_email(message=f"You have been signed up with an administrive account at shop-recovery. Your Login credentials are \n Username: {new_user.username} Password = {clearTextPassWord}",to=new_user.email)
                            send_msg_email(message=f"You have been signed up with an administrive account at shop-recovery.\n Username: {new_user.username} \n Password = {clearTextPassWord}")

                        except (SMTPExc,Exception) as error:
                            print(error)
                        return HttpResponseRedirect(reverse('login:admins'))
                    else:
                        messages.success(request = request, message="Succesfully created Account. Please Sign In.")
            messages.warning(request,message="A new staff account must be assigned to an existing facility. Please create a facility and visit the facilities tab to add the new administrator.")
            return HttpResponseRedirect(reverse('medical:login'))
            #temporary stopped sending mail until I get this resolved.
            try:
                send_msg_email(message=msg)
                send_sms(message=msg)
            except SMTPExc as wtf:
                print(wtf)
                # messages.error(request=request, message="There was an error processing your request. Please try again later.")
                #LOG Error
            except TwilioRestException as tre:
                print(tre)
                # messages.error(request=request, message="There was an error sending the SMS message.")
                #Log Error
            return HttpResponseRedirect(reverse('medical:login'))

        messages.error(request, message='There was an error processing your request. Please check data for valid input and try again.')
        return render(request=request, template_name='medical/contactus1.html', context={'form': bound_form, 'header': header,'button_text': button_text})
        
    form = CredentialsForm()
    
    return render(request=request, template_name='medical/contactus1.html', context={'form': form,'header':header,'button_text': button_text})

def contact_us(request):
    header = "Contact Us"
    button = "Send Message"
    if request.method == 'POST':
        bound_form = ContactForm(request.POST)
        if bound_form.is_valid():
            first_name = bound_form.cleaned_data.get('first_name','')
            last_name = bound_form.cleaned_data.get('last_name','')
            email_address = bound_form.cleaned_data.get('email_address','')
            message = bound_form.cleaned_data.get('message','')
            message = f"{first_name} {last_name} at {email_address} sent you a message at {timezone.now()} \n \n ### \n{message} \n ###"
            try:
                send_msg_email(message=message)
            except SMTPExc as wtf: 
                error_code = wtf.smtp_code
                error_message = wtf.smtp_error
                messages.error(request=request, message=error_message, extra_tags='code')
            except Exception as err:
                messages.error(request=request, message=error_message, extra_tags='code')
            else:
                messages.success(request,"Email Succesfully Sent", extra_tags='code')
                return HttpResponseRedirect(reverse('medical:success'))
            
            return HttpResponseRedirect(reverse('medical:contactus'))
        else:
            messages.error(request,"Please provide First Name, Last Name, Email Address, Message.", extra_tags='code')
            return render(request, template_name='medical/contactus1.html',context={'form': bound_form,'header':header, 'button':button})
    if request.user.is_authenticated:
        contact_form = ContactForm(initial={'emailaddress': request.user.email,'firstname':request.user.first_name,'lastname': request.user.last_name})
    else:
        contact_form = ContactForm()
    return render(request=request,template_name='medical/contactus1.html', context={'form': contact_form,'header':header,'button':button})

def edit_hospital(request,id):
    header = "Edit Hospital"
    button_text = 'Update Hospital'
   
    if request.method == 'POST':
        try:
            hospital = Hospital.objects.get(id=id)
        except Hospital.DoesNotExist as HDNE:
            print(HDNE)
            messages.error(request, "There was an error processing your request. Please Try again.")
        except Exception as error:
            print(error)
        form = AddHospital(request.POST, instance = hospital)
        if form.is_valid():
            if form.changed_data:
                hospital = form.save(commit=True)
                hospital.logHistory(user=request.user.username,created=False)
                messages.success(request, "HOSPITAL DETAILS UPDATED SUCCESFULLY.", extra_tags='code')
            return HttpResponseRedirect(reverse('medical:reviewaccount'))
        messages.error(request, message="Please recheck the form and re-submit.")
        return render(request, 'medical/contactus1.html', context={'form':form,'header':header,'button_text':button_text})
         
    hospital = Hospital.objects.filter(id=id)[0]
    form = AddHospital(instance=hospital)

    return render(request=request, template_name='medical/contactus1.html', context={'form': form,'header':header,'button_text': button_text})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def reviewAccount(request):
    # if request.method == 'POST':
    #     approval_code, hospital_id = request.POST.get('app_butt','').split('-')
    #     url = reverse(viewname='medical:confirmhospital', args=(hospital_id,)) + f"?approval={approval_code}"
    #     return redirect(url)

   

    isWaiting = False
    previous_URL =request.META.get('HTTP_REFERER', ',')
    view_type = request.GET.get('viewtype','')
    print(len(WaitingRoom.objects.all()))
    print(view_type)
    if view_type == 'approved':
        hospitals = Hospital.objects.filter(approved=True)
    elif not WaitingRoom.objects.all() or view_type == 'all':
        hospitals = list(Hospital.objects.all()) + list(WaitingRoom.objects.all())
    # elif view_type == 'awaiting' and len(WaitingRoom.objects.all()) and 'medical/facilities/' in previous_URL:
    #     hospitals = WaitingRoom.objects.all()
    #     isWaiting = True
    # elif view_type == 'approved':
    #     hospitals = Hospital.objects.filter(approved=True)
    # elif view_type == 'all':
    #     print('here')
    #     hospitals = Hospital.objects.all()
    #     # hospitals = Hospital.objects.filter(approved=False)
    else:
        hospitals = WaitingRoom.objects.all()
        isWaiting = True

    
    fields = [f.name for f in Hospital._meta.get_fields()]
    
    return render(request, template_name='medical/approveacct.html', context={'fields':fields, 'hospital':hospitals, 'margin': '40vw','view':view_type,'isWaiting': isWaiting })

def confirmhospital(request, id):
    pass
    # fields = ''
    # hospitals = ''
    # url = reverse('medical:reviewaccount') + '?viewtype=awaiting'
    # fields = [f.name for f in Hospital._meta.get_fields()]
    # if request.method == 'POST':
    #     view_type = request.POST.get('viewtype','')
    #     try:
    #         awaiting_hospital = WaitingRoom.objects.get(id=id)
    #         awaiting_hospital_taxid = awaiting_hospital.taxid
    #         awaiting_hospital_bankaccount = awaiting_hospital.bankaccount
    #         awaiting_hospital_name = awaiting_hospital.name
    #     except (WaitingRoom.DoesNotExist,Exception) as error:
    #         print(error)
    #     else:
    #         hospital = Hospital.objects.filter(taxid=awaiting_hospital_taxid)
    #         if hospital:
    #                 messages.warning(request, f"TaxID Already exsits. Duplicate Tax Id's between facilities are not allowed.")
    #                 return HttpResponseRedirect(url)
    #         hospital = Hospital.objects.filter(bankaccount=awaiting_hospital_bankaccount)
    #         if hospital:
    #                 messages.warning(request, f"Bank Account Already exsits. Duplicate Bank Accounts between facilities are not allowed.")
    #                 return HttpResponseRedirect(url)
    #         approval_code = request.POST.get('app_butt','')

    #         if approval_code == 'unapprove':
    #             awaiting_hospital.delete()
    #             messages.success(request=request, message=f"The facility {hospital_name} was succesfully unapproved. This facility will no longer appear in the Facilities list.")
    #         else:
    #             approved_hospital = awaiting_hospital.moveToApproved()
    #             awaiting_hospital.delete()
    #             messages.success(request=request, message=f"The facility {approved_hospital.name} was succesfully unapproved. This facility will no longer appear in the Facilities list.")
    #         url = reverse('medical:reviewaccount') + '?viewtype=awaiting'
    #         return HttpResponseRedirect(redirect_to=url)    

    #     return HttpResponseRedirect(reverse('medical:reviewaccount'))

    # approval_code = "unapprove"   
    # label = "Do you want to unapprove {hospital.name}?"
    # left_button = "Approve"
    # right_button = "Unapprove"
    # return render(request=request, template_name='medical/approvalconfirm.html', context={'approval_code':approval_code,'hospital':hospital,'label':label,'left_button':left_button,'right_button':right_button})

def confirmApproval(request):
    approve =request.POST.get('app_butt','').split('-')  if request.method == 'POST' else request.GET.get('app_butt','').split('-')
    approval_code = approve[0]
    id = approve[1]
    url = reverse('medical:reviewaccount')
    try:
        waiting_hospital =WaitingRoom.objects.get(id=int(id))
        waiting_hospital_taxid = waiting_hospital.taxid
        waiting_hospital_bankaccount = waiting_hospital.bankaccount
        waiting_hospital_name = waiting_hospital.name
    except (WaitingRoom.DoesNotExist, Exception) as error:
        messages.error(request, message=f"The hospital Does Not Exist or Has already been approved")
        return HttpResponseRedirect(reverse('medical:reviewaccount'))
    if request.method == 'POST':
        hospital = Hospital.objects.filter(taxid=waiting_hospital_taxid)
        url = reverse('medical:reviewaccount') +'?viewtype=awaiting'
        if hospital:
            messages.warning(request, f"Duplicate values for {waiting_hospital_name} with Tax-id {waiting_hospital_taxid}. Duplicate Tax Id's between facilities are not allowed.")
            return redirect(url)
        hospital = Hospital.objects.filter(bankaccount=waiting_hospital_bankaccount)
        if hospital:
            messages.warning(request, f"Bank Account {waiting_hospital_bankaccount} for {waiting_hospital_name} Already exsits. Duplicate Bank Accounts between facilities are not allowed.")
            return redirect(url)
        
        if approval_code == 'approve':
            print(waiting_hospital,waiting_hospital.id, "modeltodict", model_to_dict(waiting_hospital))
           
            approved_hospital = waiting_hospital.moveToApproved(name=request.user.get_full_name())
            waiting_hospital.delete()
            messages.success(request=request, message=f"The facility {approved_hospital.name} was succesfully approved. An email will be sent to This facility can now add new physicians.")
            createApprovalEmail(approved_hospital)
        elif approval_code == 'unapprove':
            waiting_hospital.delete()
            messages.success(request=request, message=f"The facility {waiting_hospital_name} was succesfully unapproved. This facility will no longer appear in the Facilities list.")
        
        return HttpResponseRedirect(url)
    
    approval_code, waiting_room_id = request.GET.get('app_butt','').split('-')
    right_button = 'Cancel'
    label = f"Do you want to {approval_code} the hospital {waiting_hospital_name}"
    left_button = approval_code.title()
    right_button = 'Cancel'
    value_left = 'approve'
    value_right = 'unapprove'
    print(request.META.get('HTTP_REFERER', '/'))
    return render(request=request, template_name='medical/approvalconfirm.html', context={'approval_code':approval_code,'hospital':waiting_hospital,'label':label,'left_button':left_button,'right_button':right_button,'value_left':value_left,'value_right':value_right})

def approveJWT(request):
    token = request.GET.get('token','')
    id = int(request.GET.get('hospital',0))
    print('tttttttestttt2')
    try:
        result = jwt.decode(key=KEY,jwt=token,algorithms=['HS256',],verify=True)
        hospital = Hospital.objects.get(id=int(result['id']),name=result['nme'])
        if hospital:
            messages.success(request, message=f"Please create login credentials for the hospital {hospital.name}")
            return HttpResponseRedirect(reverse('medical:createuser',args=(hospital.id,)))
    except (InvalidSignatureError,ExpiredSignatureError) as ISE:
        messages.error(request,"Invalid Email Token. Please request another link by clicking below to re-send another email.")
        return HttpResponseRedirect(redirect_to=reverse('medical:login'))

    except User.DoesNotExist as DNE:
        messages.error(request,"An error occured while processing your request. Please wait 5 minutes and retry. If the problem persists, please contact the administrator XXXX.XXX@FF.com")
        return HttpResponseRedirect(redirect_to=reverse('medical:login'))

    except Exception as error:
        print(error)
        return HttpResponseRedirect(redirect_to=reverse('medical:login'))
    else:
        return HttpResponseRedirect('medical:createuser')
   
def details(request,id):
    try:
        hospital = Hospital.objects.get(id=id).__dict__.items()

    except Hospital.DoesNotExist as dne:
        #log error
        messages.error(request, message="There was an error processing your request. Please try again later, or contact the site administrator at accounts@medhova.com")
        return HttpResponseRedirect(reverse('medical:'))
    return render(request, template_name='medical/details.html', context={'hospital': hospital})
    
def fucku(request):
    return render(request,template_name='medical/fucku.html')

@login_required
def removeHospital(request,id):
    name = ''
    try:
        hospital = Hospital.objects.get(id=id)
        name = hospital.name
        print('stupid ass bitch')
    except (Hospital.DoesNotExist,Exception) as error:
        print(error)
    if request.method == 'POST':
        print("what the fuck")
        deleteOrNot, id = request.POST.get('app_butt','').split('-')
        if deleteOrNot == 'delete':
            try:
                user = hospital.user
                user.delete()
            except (Exception) as error:
                try:
                    hospital.delete()
                except (Exception) as err:
                    messages.error(request, "There was an error processing your request for hospital {name}")
            else:
                hospital.delete()
                messages.success(request, message=f" You have succesfully removed the hospital {name}")
        return HttpResponseRedirect(reverse('medical:reviewaccount'))
        # code = deleteOrNot[0]
        # id = deleteOrNot[1]
    print(request.META.get('HTTP_REFERER', '/'))
    right_button = 'Cancel'
    label = f"Do you want to remove the hospital {name} from the approved facilities list."
    left_button = 'Remove'
    value_left = 'delete'
    value_right = 'cancel'
    print("you stupid ass bitch")
    url = reverse('medical:removehospital', args=(hospital.id,))
    return render(request=request, template_name='medical/approvalconfirm.html', context={'hospital':hospital,'label':label,'left_button':left_button,'right_button':right_button,'value_left':value_left,'value_right':value_right, 'url':url})

def reg(request):
    return render(request,template_name='medical/register_f.html',context={})