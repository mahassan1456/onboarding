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
from pproducts.forms import AddProducts, AddProductTags,ProductTags,Product
from .utility_functions import returnExcelResponse
import pandas as pd
from pproducts.models import Physician
from superuseractions.models import UserHistoryTable
from quickstart.models import quickStartHospital1, quickStartPhysician
from medical.models import Hospital2

# def dumbbitch(request):
#     return HttpResponse("hello world")

def contactUs(request):

    return HttpResponse(content=f"This is the future Contact Us Page")

def downloadXLSStupidDuxkingfdumbfuckingbitch(request):
    print('fuck u stupid bitch')
    return HttpResponse(content='hello world')

def downloadXLS(request):
    datatype = request.GET.get('datatype', '')
    dataframe = ''
    sheet = ''
    file_name = ''
    physicians_=''
    physicians = ''
    prod = ''
    physicians_search_set = ''
    
    if datatype:
        search = request.GET.get('search','')
        searchTerms = search.split()
        qs = request.GET.get('qs','')
        if datatype == 'physicians':
            print('physisisisicans')
            if search:
                if qs:
                    print("qs",qs,"qs")
                    for i in range(len(searchTerms)):
                        if i == 0:
                            physicians = quickStartPhysician.objects.filter(first_name__icontains=searchTerms[i])
                            print('i-',i,'physician',physicians)
                        else:
                            physicians = physicians | quickStartPhysician.objects.filter(first_name__icontains=searchTerms[i])
                        physicians = physicians | quickStartPhysician.objects.filter(last_name__icontains=searchTerms[i])
                        physicians = physicians | quickStartPhysician.objects.filter(specialty__tag__icontains=searchTerms[i])
                        physicians = physicians | quickStartPhysician.objects.filter(email__icontains=searchTerms[i])
                else:
                    print("not_qs")
                    physicians_u = Physician.objects.filter(sd=False)
                    for i in range(len(searchTerms)):
                        if i == 0:
                            physicians_search_set = physicians_u.filter(facility__name__icontains=searchTerms[i])
                        else:
                            physicians_search_set = physicians_search_set | physicians_u.filter(facility__name__icontains=searchTerms[i])
                        physicians_search_set = physicians_search_set | physicians_u.filter(specialty_ph__tag__icontains=searchTerms[i])
                        physicians_search_set = physicians_search_set | physicians_u.filter(firstName__icontains=searchTerms[i])
                        physicians_search_set = physicians_search_set | physicians_u.filter(lastName__icontains=searchTerms[i])
                    physicians_ = physicians_search_set
                   
            else:   
                try:
                    hospital_id = request.GET.get("selected_hospital",'')
                    if hospital_id == 'all':
                        physicians_ = Physician.objects.all()
                        print('wrong',physicians_)
                        sheet = 'physicians_all.xlsx'
                    else:
                        hosp = Hospital.objects.filter(id=int(hospital_id))[0]
                        physicians_ = hosp.physician_set.filter(sd=False)
                        print('correct',physicians_)
                        sheet = f"{hosp.name}.xlsx"
                except (Physician.DoesNotExist,Exception) as error:
                    print(error)
                    return
            objects = physicians_
            file_name = 'physicians.xlsx'

        elif datatype == 'products':
            print('here')
            datatype = request.GET.get('datatype','')
            specialty = request.GET.get('selected_specialty','')
            try:
                if specialty == 'all':
                    products = Product.objects.all()
                else:
                    products =ProductTags.objects.get(tag=specialty).products.all()
                print(products)
                dataframe = pd.DataFrame(products.values()).set_index('id')
                sheet = 'products'
                file_name = 'products.xlsx'

                dataframe['created_at'] = dataframe['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
                dataframe['updated_at'] = dataframe['updated_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            except (Exception) as error:
                print(error)
                return HttpResponse(f"{error}")
            else:
                return returnExcelResponse(dataframe=dataframe,sheet=sheet, file_name=file_name)

        elif datatype == 'specialty':
            print('here3')
            product = request.GET.get('selected_product','')
            print('product',product)
            
            if product == 'all':
                tags = ProductTags.objects.all()
            else:
                prod = Product.objects.get(name=product)
                tags =prod.specialties.all()
            
            dataframe = pd.DataFrame(tags.values()).set_index('id')
            sheet = prod.name
            file_name = f"{prod.name}.xlsx"

            dataframe['created_at'] = dataframe['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            dataframe['updated_at'] = dataframe['updated_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            
            return returnExcelResponse(dataframe=dataframe,sheet=sheet, file_name=file_name)
        elif datatype == 'hospital':
            if qs:
                if search:
                    for i in range(len(searchTerms)):
                        if i == 0:
                            hospitals = quickStartHospital1.objects.filter(hospital_name__icontains = searchTerms[i])
                        else:
                            hospitals= hospitals| quickStartHospital1.objects.filter(hospital_name__icontains = searchTerms[i])
                        hospitals = hospitals | quickStartHospital1.objects.filter(hospital_zip__icontains=searchTerms[i])
                        hospitals = hospitals| quickStartHospital1.objects.filter(user__email__icontains=searchTerms[i])
                        hospitals = hospitals | quickStartHospital1.objects.filter(user__email__icontains=searchTerms[i])
                else:
                    choice = request.GET.get('selected_hospital','')
                    print("under drop down")
                    if choice == 'Is Invited':
                        selection = 'Is Invited'
                        hospitals = quickStartHospital1.objects.filter(is_emailed=True)
                    elif choice == 'Has Physicians':
                        selection = 'Has Physicians'
                        hospitals = quickStartHospital1.objects.filter(has_physicians=True)
                    elif choice == 'Is Onboarded':
                        selection = 'Is Onboarded'
                        hospitals  = quickStartHospital1.objects.filter(is_registered=True)
                    elif choice == 'All':
                        hospitals = quickStartHospital1.objects.filter()
                    else:
                        hospitals  = Hospital2.objects.filter(is_manual=True)
                    print('hoo',hospitals)
            else:
                if search:
                    for i in range(len(searchTerms)):
                        if i == 0:
                            hospitals = Hospital2.objects.filter(name__icontains = searchTerms[i])
                        else:
                            hospitals = hospitals | Hospital2.objects.filter(name__icontains = searchTerms[i])
                        
                        hospitals = hospitals | Hospital2.objects.filter(zip__icontains=searchTerms[i])
                        hospitals = hospitals | Hospital2.objects.filter(city__icontains=searchTerms[i])
                        hospitals = hospitals | Hospital2.objects.filter(state__icontains=searchTerms[i])
                else:
                    hospitals = Hospital2.objects.filter(soft_delete=False)
            objects = hospitals
        else:
            pass
        dataframe = pd.DataFrame(objects.values()).set_index('id')
        dataframe['created_at'] = dataframe['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
        dataframe['updated_at'] = dataframe['updated_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
        return returnExcelResponse(dataframe=dataframe,sheet=sheet, file_name=file_name)
        # else:
        #     print('fffff')
        #     from medical.models import Hospital2
        #     hospitals = Hospital.objects.all().defer('created_at','modified_at')
        
            
        #     dataframe = pd.DataFrame(hospitals.values()).set_index('id')
        #     dataframe[['modified_at','created_at','approved_at']]=dataframe[['modified_at','created_at','approved_at']].astype(str)
        #     sheet = 'hospitals'
        #     file_name = 'hospitals'

        # return returnExcelResponse(dataframe=dataframe,sheet=sheet, file_name=file_name)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def addProduct(request):
    
    if request.method == 'POST':
        print(request.POST)
        form = AddProducts(request.POST,request.FILES)
        if form.is_valid():
            specialties = form.cleaned_data.get('specialties','')
            
            product = form.save()
            product.specialties.add(*specialties)
            product.save()
            if product:
                log_record = UserHistoryTable.objects.create(action="1",page_link=f"/views/product/detail/{product.id}/",entity_type='Product',entity_name=product.name,entity_id=product.id,action_verbose=f" w/Specialties {product.buildSpecialtiesString()} ")
                log_record.user = request.user
                log_record.save()
                request.user.save()
           
            messages.success(request,message=f"Succesfully added {product.name} to the products Database.")
            return HttpResponseRedirect(reverse('dashboard:master_dashboard'))
        print(form.errors)
        return render(request,template_name='support/add_new_product.html',context={'form':form})
    form = AddProducts(initial={'pushtowoo':""})
    return render(request,template_name='support/add_new_product.html',context={'form':form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def addSpecialty(request):
    x=12
    if request.method == 'POST':
        form = AddProductTags(request.POST,request.FILES)
        if form.is_valid():
            print(request.POST)
            specialty = form.save()
            print('specialty-name',specialty.tag)
            print('products-all',specialty.products.all())
            messages.success(request,message=f"Succesfully added Specialty {specialty.tag} with associated products {specialty.products.all()}")
            return HttpResponseRedirect(reverse('dashboard:master_dashboard'))
        print(form.errors)
        return render(request,template_name='support/add_specialty.html',context={'form':form})
    form = AddProductTags()
    return render(request,template_name='support/add_specialty.html',context={'form':form})

def addHospital(request):
    pass

# def addPhysician(request):
#     pass

@login_required    
def addPhysician(request):

    from pproducts.forms import AddPhysician, AddPhysicianAdmin
    # Flag for template to know we are adding a new physician and to render the HTML accordingly
    new = True
    # Flag for template to know we are adding a new physician and to render the HTML accordingly
    # Query Parameter 'new' is passed from the href in the physicians_view to the form to render the form as a new physician sign up
    editornew = request.GET.get('edit', False)
    # Get all tags to display to user to choose specialties.
    tags = ProductTags.objects.all()
    header = 'Add Physician'
    button_text = 'Add Physician'
    state = {}
   
    if request.method == 'POST':
     
        
      
        if request.user.is_superuser:
            try:
                facility = request.POST.get('hospital', False)
                hospital = Hospital.objects.get(id=facility if facility else 0)
                form = AddPhysicianAdmin(request.POST, request.FILES,new=True)
            except (Hospital.DoesNotExist,ValueError) as hdne:
                messages.error(request, "Error Assigning to Hospital. Please Contact Administrator ")
                return HttpResponseRedirect(reverse('pproducts:addphysician'))
            else:
                print("does it make iteweqewqew")
                if form.is_valid():
                    print('request.post',request.POST)
                    pushtowoo = request.POST.get('pushtowoo','')
                    #test if specialty_ph is none which means they filled out nothing
                    post = dict(request.POST)
                    post.update(form.cleaned_data)
                    post.pop('csrfmiddlewaretoken')
                    physician = form.save(post,hospital=hospital ,commit=True, admin=request.user,action='Created')
                    created,products =physician.buildProductsSet(data=request.POST,created=True)
                    if physician:
                        page_link = f"/views/physician/detail/{physician.id}/"
                        record = UserHistoryTable.objects.create(action='1',change_type='physician',action_verbose="New",
                                                                 entity_type='Physician',entity_name=physician.get_full_name(),entity_id=physician.id, page_link=page_link)
                        record.user = request.user
                        record.save()
                        request.user.save()
                    print('record',record)

                    messages.success(request, f"Successfully added a physician {physician.firstName} {physician.lastName}")
                    return HttpResponseRedirect(reverse('dashboard:master_dashboard'))
                else:
                   
                    messages.warning(request,"Please Review Errors and Resubmit form.")
                    print(form.errors,'errors')
                    return render(request,template_name='support/add_physician_f.html',context={'form':form,'button_text': button_text, 'header': header,'tags':tags,'new':new})

        else:
            # CHECK FOR ERRORSSSSSSSSSS
            form = AddPhysician(request.POST, request.FILES)
            print(request.POST)
            if form.is_valid():
                post = dict(request.POST)
                post.update(form.cleaned_data)
                post.pop('csrfmiddlewaretoken')
                print(post)
                physician = form.save(post,hospital = request.user.hospitals.all()[0],commit=True,admin = request.user, action='Created')
                created,products = physician.buildProductsSet(data=request.POST,created=True)
                print(post)
                if physician:
                    state = physician.checkState(new=True)
                    record = UserHistoryTable.objects.create(action='1',change_type='physician',action_verbose=f" Physician {physician.get_full_name()} @ {physician.facility.name}",action_obj=state)
                    record.user = request.user
                    record.save()
                    request.user.save()
                    print('record',record)
                    msg = f"Successfully added a physician {physician.firstName} {physician.lastName}"
                if request.user.is_superuser:
                    msg = f"Successfully added a physician {physician.firstName} {physician.lastName} @ {physician.facility.name}"
                    return HttpResponseRedirect(reverse("dashboard:master_dashboard"))
                messages.success(request=request,message= msg)
                return HttpResponseRedirect(reverse("dashboard:dashboard"))
            # If form is not valid for a regular staff user please submit a warning.
            else:
                messages.warning(request,"Please Review Errors and Resubmit form.")
                print(form.errors)
                return render(request, template_name='support/add_physician_f.html',context={'form':form,'button_text': button_text, 'header': header,'tags':tags,'new':new})
    # render the form depending on the type of user adding the physician
    if request.user.is_superuser:
        form = AddPhysicianAdmin(new=True)
    else:
        form =AddPhysician(initial={'hospital':request.user.hospitals.all()[0]},new=True)

    tags = ProductTags.objects.all()

    return render(request, template_name='support/add_physician_f.html', context={'form':form, 'tags':tags, 'button_text': button_text, 'header': header})
    # return render(request, template_name='pproducts/addphysician.html', context={'form':form, 'button_text': button_text, 'header': header,'hoe':'whttheufk'})
