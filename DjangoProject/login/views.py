from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout as logout_user
from django.contrib.auth import login as login_user
from django.contrib.auth.models import User
from login.utility_functions import *
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from login.forms import *
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
import jwt
from email.mime.text import MIMEText
from smtplib import  SMTPResponseException as SMTPExc
from twilio.base.exceptions import TwilioException, TwilioRestException
import datetime
from mysite.settings import SECRET_KEY as KEY
from login.utility_functions import send_forgot_password,send_approve_hospital
from django.contrib.auth.hashers import make_password, check_password
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError
from medical.forms import *
from medical.models import *
import jwt
from mysite.settings import SECRET_KEY as KEY
from login.models import WaitingRoom
from medical.forms import Login,ApproveFromLogin




# Create your views here.

def loginUser(request):
    header = "Welcome Back"
    button_text = "Login"
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
            
        return render(request,'login/login.html', context={'form':form,'button_text':button_text})

    user = False
    form = Login()
    return render(request, 'login/login.html',context={'form': form,'header':header,'button_text':button_text})

def logout(request):

    logout_user(request)
    return HttpResponseRedirect(reverse('medical:login'))

def register1(request, id=None):
    
    header = "Add Facility"
    button = "Create New Facility"
    if request.method == 'POST':
        if request.user.is_superuser:
            form = AddHospital(request.POST)
        else:
            form = WaitingRoomForm(request.POST)
        
        if form.is_valid():
            hospital = form.save(commit=True)
            if request.user.is_authenticated:
                messages.success(request, f"Sucessfully Added Hospital {hospital.name}.",extra_tags='success')
                return HttpResponseRedirect(reverse('medical:dashboard'))
            try:
                send_approve_hospital(hospital=hospital)
                messages.success(request, f"A request has been sent to the administrator for approval. Once approval has been confirmed you will receive an email containing instructions and a link to establish log in credentials",extra_tags='success')
                return HttpResponseRedirect(reverse('medical:login'))
            except (SMTPExc, Exception) as error:
                print(error)
                messages.error(request,f"There was an error processing your request. Please contact the administrator for more details.")
                return HttpResponseRedirect(reverse('medical:contactus'))
            return HttpResponseRedirect(reverse('medical:login'))
    
        return render(request, 'medical/contactus1.html', context={'form':form,'header':header,'button':button})

    if request.user.is_superuser:
        form = AddHospital()
    else:    
        form = WaitingRoomForm()
    
    return render(request, 'medical/contactus1.html', context={'form':form,'header':header, 'button_text': 'Add Facility'})
@login_required
def createProfile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UserProfileAdminForm(request.POST,request.FILES,instance=request.user.userprofileadmin)
            if form.is_valid():
                userProfile = form.save(commit=True)
                messages.success(request,message="Succesfully Updated Profile.",extra_tags='success')
                return HttpResponseRedirect(reverse('medical:dashboard'))
    button_text = "Update Profile"
    
    header = "Update Profile"
    id = request.GET.get('id',0)
    print(id)
    if id:
        try:
            user = User.objects.get(id=int(id))
        except (User.DoesNotExist, Exception) as HDNE:
            
            messages.error(request, message=f"Error Occurred While Processing Request")
            return HttpResponseRedirect('medical:dashboard')
    if request.method == 'POST':
        if request.user:
            try:
                form = UserProfileAdminForm(request.POST,request.FILES,instance=user.userprofileadmin)
            except (NameError,Exception) as error:
                print(error)
        else:
            form = UserProfileAdminForm(request.POST,request.FILES,instance=request.user.userprofileadmin)
        if form.is_valid():
         
            userProfile = form.save(commit=True)
            
            return HttpResponseRedirect(reverse('medical:dashboard'))

        return render(request,template_name='medical/contactus1.html', context={'form':form,'button_text':button_text,'header':header} )
    if id:
        try:
            user = User.objects.get(id=id)
        except (User.DoesNotExist, Exception) as HDNE:
            print(HDNE)
            messages.error(request, message=f"Error Occurred While Processing Request")
            return HttpResponseRedirect('medical:dashboard')
        form = UserProfileAdminForm(instance=user.userprofileadmin)
    else:
        form = UserProfileAdminForm(instance=request.user.userprofileadmin)
    return render(request,template_name='medical/contactus1.html', context={'form':form,'button_text':button_text,'header':header, 'function':'editprofile'} )

def forgot_password(request):
    header = "Forgot Password?"
    button_text = "Reset Password"
    reset_text = "Please input your registered email addresss on  to receive a password request link. Check your spam mail if the email has not arrived."
   
    if request.method == 'POST':
        form = ForgotLogin(request.POST)
        if form.is_valid():
            try:
                print(form.cleaned_data)
                email = form.cleaned_data.get('email',"")
                requested_user = User.objects.get(email=email)
            except (User.DoesNotExist, KeyError) as Error:
                print(Error)
                result1 = True
            except Exception as Error:
                print("Error")
            else:
                send_forgot_password(requested_user=requested_user)

        messages.success(request=request,message=f"If a record exists a password reset link will be sent to {email} ",extra_tags='success')
        return render(request, 'login/login.html', context={'form':form,'header':header,'button_text': button_text,'reset_text':reset_text})
    form = ForgotLogin()
    return render(request, 'login/login.html', context={'form':form,'header':header,'reset_text':reset_text,'button_text':button_text})

def reset_password(request):

    #verify if jwt is okay and also
    token = request.GET.get('token','')
    try:
        user = User.objects.get(username=request.GET.get('uname'))
        result = jwt.decode(key=KEY,jwt=token,algorithms=['HS256',],verify=True)

    except (InvalidSignatureError,ExpiredSignatureError) as ISE:
        messages.error(request,"Invalid Email Token. Please request another link by clicking below to re-send another email.",extra_tags='warning')
        return HttpResponseRedirect(redirect_to=reverse('polls:forgot_password'))

    except User.DoesNotExist as DNE:
        print(DNE)

    except Exception as error:
        print(error)

    else:
        if request.method == 'POST':

            form = ResetPassword(request.POST)
            if form.is_valid():

                password1 = form.cleaned_data.get('password1','')
                password2 = form.cleaned_data.get('password2','')

                if password1 == password2:

                    password = make_password(password=password1)
                    user.password = password
                    user.save()
                    messages.success(request,"Password Succesfully Changed",extra_tags='success')
                    return HttpResponseRedirect(reverse('medical:login')) 
            
            return render(request,template_name='medical/login1.html',context={'form':form})

    messages.info(request, "Please enter new Password")
    form = ResetPassword()
    return render(request,template_name='medical/login1.html',context={'form':form})

@login_required
def admins(request):
    data_label = 'admin'
    if not request.user.is_superuser:
        messages.error(request,message='Only superusers can view admin information.')
        return HttpResponseRedirect(reverse('medical:dashboard'))
    admin_staff = User.objects.all().exclude(is_superuser=True).order_by('last_name')
    hospitalPresent = admin_staff.values_list('hospital2')
    admin_staff = [(admin_staff[i], hospitalPresent[i][0]) for i in range(len(admin_staff))]
    


    print(admin_staff)
    return render(request,template_name='login/admins_page.html',context={'admin_staff':admin_staff,'data_label':data_label})
@login_required
def editAdmin(request,id):
    header = "Edit Administrator"
    button = "Update Details"
    try:
        admin = User.objects.get(id=id)
    except (User.DoesNotExist, Exception) as error:
        print(error)
    if request.method == 'POST':
        form = CredentialsFormAdmin(request.POST,instance=admin)
        if form.is_valid():
            admin = form.save(commit=True)
            messages.success(request=request, message=f"You have succesfully edited {admin.first_name} {admin.last_name}",extra_tags='success')
            return HttpResponseRedirect(reverse('login:admins'))
        return render(request,template_name='medical/contactus1.html',context={'form':form,'button':button,'header':header})
    form = CredentialsFormAdmin(instance=admin)
    return render(request,template_name='medical/contactus1.html',context={'form':form,'button':button,'header':header})
@login_required
def removeAdmin(request,id):

    admin = User.objects.filter(id=id)[0]

    if request.method == 'POST':
        
        first_name = admin.first_name
        last_name = admin.last_name
        hospital = admin.hospital2.name
        value = request.POST.get("approval", "")

        if value:
            del_admin = admin.delete()
        
            messages.success(request, message=f"You have succesfully deleted Administrator: First: {first_name} Last: {last_name} @ Hospital {hospital}",extra_tags='success')
        
        return HttpResponseRedirect(reverse('login:admins'))

    label = f"Do you want to remove First: {admin.first_name} Last: {admin.last_name} @ {admin.hospital2.name}."
    return render(request=request,template_name='pproducts/removephysician.html',context={'label':label})



# if request.method == 'POST':

#         form = Login(request.POST)

#         if form.is_valid():
#             username = form.cleaned_data.get('username','').lower()
#             password = form.cleaned_data.get('password','')

#             user = authenticate(request,username=username,password=password)
#             url = request.GET.get('next', '')
            
#             if user is not None:
#                 login_user(request, user)
#                 return HttpResponseRedirect(url if url else reverse('medical:dashboard'))
#             else:
#                 messages.error(request, "Username or Password is Incorrect", extra_tags='code')
            
#             return render(request,'medical/login1.html', context={'form':form})

#     user = False
#     form = Login()
#     return render(request, 'medical/login1.html',context={'form': form,'header':header})
def approveHospitalFromLink(request):

    
    header = "Submit Approval"
    fromEmailLink = True
    if request.method == "POST":
        form = ApproveFromLogin(request.POST)
        approval = request.POST.get('app_butt','').split('-')
        approval_code = approval[0]
        id = approval[1]
        print(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username','')
            password = form.cleaned_data.get('password','')
            user = authenticate(request,username=username,password=password)

            if user is not None:
                try:
                    waiting_hospital = WaitingRoom.objects.get(id=int(id))
                except (WaitingRoom.DoesNotExist,Exception) as hdne:
                    print(hdne)
                    return HttpResponse("<h2> There was an error processing your request. Please log in or try again later.<h2>")
                else:
                    if approval_code == 'approve':
                        hospital = waiting_hospital.moveToApproved(name=user.get_username())
                        waiting_hospital.delete()
                    else:
                        waiting_hospital.delete()
                    return HttpResponse(f"<h2 style='text-align:center;'> The hospital {hospital.name} was succesfully approved by {user.get_username()} <h2>")
                
            else:
                messages.error(request,message="Incorrect Password or Username. Please try again.")
                return render(request, 'medical/login1.html',context={'form': form,'header':header,'fromEmailLink':fromEmailLink,'button':'submit'})
    token = request.GET.get('token','')
    print(token)
    try:
        result = jwt.decode(key=KEY,jwt=token,algorithms=['HS256',],verify=True)
        print(result)
        waiting_hospital = WaitingRoom.objects.get(id=int(result['id']),name=result['nme'],street=result['str'])
        print('waitinghospital',waiting_hospital)
        name = ''
        if waiting_hospital:
            print("testinggggg")
            form = ApproveFromLogin()
            return render(request, 'medical/login1.html',context={'form': form,'header':header,'fromEmailLink':fromEmailLink,'button':'submit','hospital': waiting_hospital})      

    except (InvalidSignatureError) as ISE:
        return HttpResponse("Invalid Token. Please login in to Shop-Recovery to submit approval.")

    except WaitingRoom.DoesNotExist as dne:
        print(dne)
        return HttpResponse("An error occured while processing your request. Please wait 5 minutes and retry. If the problem persists, please contact the administrator XXXX.XXX@FF.com")
    except ExpiredSignatureError as experror:
        messages.error(request,"Expired token. Please login in to shop-recovery to submit approval.")
        print(experror)
        return HttpResponse(content="<h2> Expired token. Please login in to shop-recovery to submit approval.<h2>")

    except Exception as error:
        return HttpResponse(content="<h2> An Error Occurred. Please Log in and approve.<h2>")
   
