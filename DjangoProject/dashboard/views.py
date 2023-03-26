from django.shortcuts import render

from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from smtplib import  SMTPResponseException as SMTPExc
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from mysite.settings import SECRET_KEY as key
from register.forms import AddHospital
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout as logout_user
from django.forms.models import model_to_dict
from pproducts.models import Physician, Product
from medical.models import Hospital2
from django.core.exceptions import ObjectDoesNotExist
from quickstart.models import quickStartHospital1
from superuseractions.models import UserHistoryTable
from django.contrib.auth.models import User 



# Create your views here.

@login_required
def master_dashboard(request):
    dashboard = 1
    # Obtain counts from the database for Products, Physicians, Hospitals
    hospital_count = Hospital2.objects.count()
    physician_count = Physician.objects.count()
    product_count = Product.objects.count()
    #  Obtain the most recent 5 hospital onboarded and the most recent 5 physicians added to render to dashboard.
    log_set = UserHistoryTable.objects.all().order_by('-action_time')[0:5]
    physician_set = Physician.objects.filter(sd=False).order_by('-created_at__second')[0:5]
    hospital_set =  Hospital2.objects.filter(soft_delete=False)
    return render(request=request,template_name='dashboard/master_dashboard.html',context={'physician_set':physician_set,'hospital_set':hospital_set,'hospital_count':hospital_count,'physician_count':physician_count,'product_count':product_count,'dashboard':dashboard,'log_set':log_set})

@login_required
def dashboard(request):
    left_button = "Update Profile"
    right_button = "Cancel"
    heading = "Complete Profile"
    updateProfile = True
    message = "Please Update your information"
    physician_set = request.user.hospitals.all()[0].physician_set.filter(sd=False)
    try:
        invited_physician_set = request.user.qs_hospital.qs_physicians.filter(is_recommending=False)
        invited_physician_set = invited_physician_set | request.user.hospitals.all()[0].qsp.filter(is_recommending=False)
    except (quickStartHospital1.DoesNotExist,ObjectDoesNotExist,Exception):
        invited_physician_set = []
    if not request.user.userprofileadmin.mobile_contact:
        messages.warning(request,f"Please add your Mobile Contact Information in the User Profile section or by clicking here",extra_tags='warning')
    return render(request=request,template_name='dashboard/hospital_dashboard_.html',context={'physician_set':physician_set,'invited_physician_set':invited_physician_set,"message":message,"heading":heading,"updateProfile":updateProfile})
@login_required
def updateInformationUser(request,id):
    print("helllo mfer")
    try:
        user = User.objects.get(id=id)
    except (User.DoesNotExist,Exception) as error:
        print(error)
        return HttpResponse("Error Processing Request")
    sub_but = request.POST.get('sub_but','')
    value = request.POST.get("update",'')
    print('value',value,'sub_but',sub_but)
    try:
        if sub_but == 'email':
            user.email = value
        elif sub_but == 'mobile':
            profile = user.userprofileadmin
            profile.mobile_contact = value
            user.save()
            profile.save()
            print(user.userprofileadmin.mobile_contact,'mobilecontact')
        else:
            user.last_name = value
        user.save()
    except Exception as error:
        print(error)
        messages.error(request,message=f"Error Processing Request.",extra_tags='warning')
    else:
        messages.success(request,message=f"Succesfully updated Profile Information.",extra_tags='success')
    return HttpResponseRedirect(reverse('dashboard:dashboard'))



def logout(request):
    logout_user(request)
    return HttpResponseRedirect(reverse('register:login'))

def test(request):
    products = Product.objects.all()
    return render(request,template_name='dashboard/components/ttt.html',context={'product_set':products})
