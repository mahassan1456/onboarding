from django.shortcuts import render
from pproducts.models import Specialty, ProductTags, Product,Physician
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.core import serializers
import json
from smtplib import  SMTPResponseException as SMTPExc
from io import BytesIO as IO
import pandas as pd
from django.forms.models import model_to_dict
from django.contrib import messages
from django.urls import reverse
from medical.models import Hospital2
from pproducts.forms import AddProduct2Physician, AddProducts, AddProductTags,AddTags2PhysicianForm, AddHospitalAdmin, LinkedProductTags
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from mysite.settings import ADMIN_CONTACT
from django.contrib.auth.models import User
from quickstart.models import quickStartHospital1 as quickStartHospital,quickStartPhysician
from quickstart.forms import QuickStartHospitalInvite,QuickStartPhysicianForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from quickstart.utility_functions import buildJWTQuickStartHospital,buildJWTQuickStartPhysician
from quickstart.utility_functions import send_msg_email
from superuseractions.models import UserHistoryTable
from views.utility_functions import returnSearch
from superuseractions.models import QuickInviteLogs
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

SEARCHMAPPING = {"physician":{"product":"productitems__name__istartswith","last name":"lastName__istartswith","first name":"firstName__istartswith","hospital":"facility__name__istartswith","specialty":"specialty"},
                     "product":{"specialty":"specialties__tag__istartswith", "product":"name__istartswith","physician":"physician__lastName__istartswith"},
                     "specialty": {"product":"products__name__istartswith","physician":"physicians__lastName__startswith","specialty":"tag__istartswith" },
                     "activity_logs": {"action":"action__istartswith","entity_name":"entity_name__istartswith","entity_type":"entity_type__istartswith","user":"user__email__istartswith"},
                    }

ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def view_activity(request):
    # if request.method == 'POST':
    #     log_type = request.POST.get('log_type','')
    #     if log_type== 'qs':
    #         logs = QuickInviteLogs.objects.all().order_by('-send_time')
    #     elif log_type == 'user':
    #         logs = UserHistoryTable.objects.all().order_by()
    isqsl = request.GET.get('qsl','')
    link = reverse('views:view_activity') + f"?qsl={isqsl}"
    log_set = ''
    if request.method == 'POST':
        searchTerms_raw =request.POST.get('search','')
        searchTerms =request.POST.get('search','')
        try:
            if '=' in searchTerms:
                choice = {"Deleted":"0","Updated":"2","Created":"1","Restored":"3"}
                qsl = request.GET.get('qsl','')
                category,searchTerms = searchTerms.split("=")
                if choice.get(searchTerms,''):
                    SearchTerms = choice.get(category,'')
                logs_map = SEARCHMAPPING['activity_logs']
                logs_map_new = {}
                logs_map_new[category] = {logs_map.get(category):searchTerms} 

                if qsl:
                    history = QuickInviteLogs.objects.all()
                else:
                    history = UserHistoryTable.objects.all()
                log_set = history.filter(**logs_map_new[category])
            else:
                searchTerms = searchTerms.split()
                for i in range(len(searchTerms)):
                    if i == 0:
                        log_set = UserHistoryTable.objects.filter(action=searchTerms[i])
                    else:
                        log_set = log_set |    UserHistoryTable.filter(action=searchTerms[i])

                    log_set =   log_set     |    UserHistoryTable.objects.filter(entity_name__istartswith=searchTerms[i])
                    log_set =   log_set     |    UserHistoryTable.objects.filter(entity_type__istartswith=searchTerms[i])
                    log_set =   log_set     |    UserHistoryTable.objects.filter(user__username__istartswith=searchTerms[i])
                    log_set =   log_set     |    UserHistoryTable.objects.filter(user__email__istartswith=searchTerms[i])
            
            link = reverse('views:view_activity') + f"?qsl={isqsl}"
            
        except Exception as error:
            print(error)
        else:
            messages.success(request,f"Search Results for {searchTerms_raw} returned {len(log_set)} Results",extra_tags='success')
            return render(request,template_name='views/logs_table.html',context={'log_set':log_set,'isqsl':isqsl,'searchTerms':searchTerms_raw,'link':link})

    # get query parameter in order to check which entity type is being sent from the logs_tables template. Dynamically creating columns. 
    if isqsl:
        log_set = QuickInviteLogs.objects.all().order_by('-send_time')
        isqsl= True
    else:
        log_set = UserHistoryTable.objects.all()
    return render(request,template_name='views/logs_table.html',context={'log_set':log_set,'isqsl':isqsl,'link':link})

def pushInviteLogs(request):
        pass
    
    

            



def viewProductDetail(request,id):

    try:
        product = Product.objects.get(id=id)
    except (Product.DoesNotExist,Exception) as error:
        print(error)
        return HttpResponse(f"{error}")
    
    return render(request,template_name='views/product_detail.html',context={'product':product})

def productDetailPopUp(request):
    product_id = request.POST.get('product')
    try:
        product = Product.objects.get(id=int(product_id))
    except (Product.DoesNotExist,Exception) as error:
        print(error)
        return
    
    product_dict = product.buildProductDictwImages()

    return JsonResponse(data={'dataset':product_dict})

def searchViewHospital(request):
    searchType = request.GET.get('searchType','')
    searchTerm = request.POST.get('search','')

    searchTerms = searchTerm.split()

    for i in range(len(searchTerms)):
        if i == 0:
            hospitals = Hospital2.objects.filter(name__icontains = searchTerms[i])
        hospitals = hospitals | Hospital2.objects.filter(name__icontains = searchTerms[i])
    
    return render(request=request,template_name='views/hospital_list_master_user.html',context={'hospital_set':hospitals})

def fuckuyoustupidassdumbfuckingbitch(request):
    url = ''
    qs = request.GET.get('qs','')
    soft_delete_view = ''
    physicians = ''
    status = ''
    if qs:
        filter = request.POST.get('qs_state','')
        print("enter in 1")
        if filter:
            if request.user.is_superuser:
                qsp = quickStartPhysician.objects.all()
            else:
                qsp  =  request.user.hospitals.all()[0].qsp.all() | request.user.qs_hospital.qs_physicians.all()
            print(qsp)
            if filter == 'uassgn':
                print('fuck1')
                object_set = qsp.filter(is_assigned=False)
                status = "Unassigned"
            elif filter == 'all':
                object_set = qsp
            elif filter == "onb":
                print('fuck13')
                status = "Not Onboarded"
                object_set = qsp.filter(is_onboarded=False)
            elif filter == "rmd":
                print('fuck14')
                status = "Not Recommending"
                object_set = qsp.filter(is_recommending=False)
            else:
                print('fuck15')
                status = "Complete"
                object_set = qsp.filter(is_recommending=True, is_onboarded = True)
        else:
            return JsonResponse(data={'dataset':''})
        print(object_set,'obj_set')
        physician_set = [('',phys.getHospitalName(),phys.get_full_name(),phys.buildSpecialtyString(),phys.getStatus(),phys.needsReminder(),phys.needsReminderString(),phys.id) for phys in object_set]
        
    else:
        print('req',request.POST)
        hospital_id = request.POST.get('hospital_id',0)
        print('ho',hospital_id)
        print('ho',type(hospital_id))
        if hospital_id == 'all':
            physicians = Physician.objects.filter(sd=False)
        elif hospital_id == "del":
            print("enter solve me")
            physicians = Physician.objects.filter(sd=True)
            soft_delete_view = True
            url = f"/register/remove/physician/"
        else:
            hospital_id = int(hospital_id)
            hospitals_model = Hospital2.objects.filter(id=hospital_id)
            if hospitals_model:
                physicians = hospitals_model[0].physician_set.filter(sd=False)
        print('fuclu stupid asshole')
        physician_set = [(phys.returnPictureURL(),phys.facility.name if phys.facility else '',phys.get_full_name(),phys.buildSpecialtyString(),f"/register/remove/physician/{phys.id}",f"/register/edit/physician/{phys.id}?showAll=True",phys.id) for phys in physicians]
   
    
    return JsonResponse(data={'dataset':physician_set,'deleted':soft_delete_view, 'status':status})


@login_required
def view_physicians(request):
    searchTerms_w = ''
    header = "Remove Physician"
    print('2')
    left_button = "Delete"
    right_button = "Cancel"
    action = 'delete'
    obj_type='physician'
    physicians = ''
    hospitals = Hospital2.objects.all().order_by('name')
    selectionDelete = request.GET.get('selectionDelete','')  
    if request.user.is_superuser:
        physicians_u = Physician.objects.filter(sd=True) if selectionDelete else Physician.objects.filter(sd=False)
    else:
        physicians_u = request.user.hospitals.all()[0].physician_set.all().filter(sd=False)
    print(physicians_u)
    if request.method == 'POST':
        print('3')
        searchTerms_w = request.POST.get('search','')

        if "=" in searchTerms_w:
            searchMapping = {"product":"productitems__name__istartswith","last name":"lastName__istartswith","first name":"firstName__istartswith","hospital":"facility__name__istartswith"}
            searchTerms_Z = searchTerms_w.split("=")
            category = searchTerms_Z[0].strip().lower()
            searchTerm = searchTerms_Z[1].strip()
            if searchMapping.get(category,''):
                index = {category: {searchMapping[category]:searchTerm}}
                physicians = physicians_u.filter(**index[category])
            else:
                messages.warning(request,f"Please use one of the following keys when using key word lookups ( {','.join(searchMapping.keys())} ). Example Product=Breg or first name=alan",extra_tags='warning')
                physicians = Physician.objects.none()

            # if searchTerms.lower() == "product":
            #     physicians =     physicians_u.filter(productitems__name__icontains=searchTerms[i])
        else:
            searchTerms = searchTerms_w.split()
            print('searchterms',searchTerms)
            for i in range(len(searchTerms)):
                if i == 0:
                    physicians = physicians_u.filter(facility__name__icontains=searchTerms[i])
                else:
                    physicians = physicians | physicians_u.filter(facility__name__icontains=searchTerms[i])
                physicians = physicians | physicians_u.filter(specialty_ph__tag__icontains=searchTerms[i])
                physicians = physicians | physicians_u.filter(firstName__icontains=searchTerms[i])
                physicians = physicians | physicians_u.filter(lastName__icontains=searchTerms[i])
                physicians = physicians | physicians_u.filter(productitems__name__icontains=searchTerms[i])

            print(physicians)
            # else:
            #     for i in range(len(searchTerms)):
            #         if i == 0:
            #             physicians = physicians_u.filter(facility__name__icontains=searchTerms[i])
            #             print('i-',i,'physician',physicians)
            #         else:
            #             physicians = physicians | physicians_u.filter(facility__name__icontains=searchTerms[i])
            #         physicians = physicians | physicians_u.filter(specialty_ph__tag__icontains=searchTerms[i])
            #         physicians = physicians | physicians_u.filter(firstName__icontains=searchTerms[i])
            #         physicians = physicians | physicians_u.filter(lastName__icontains=searchTerms[i])
            #         print('i-',i,'physician',physicians)
        physicians = list(set(physicians))
        return render(request=request,template_name='views/physician_list_masteruser.html',context={'object_set':physicians,'hospital_set':hospitals,'heading':header,'left_button':left_button,'right_button':right_button,'obj_type':obj_type,'action':action,'searchTerms':searchTerms_w,'qs':'' })
    print('1')
    return render(request=request,template_name='views/physician_list_masteruser.html',context={'selectionDelete':selectionDelete,'searchTerms':searchTerms_w,'object_set':physicians_u,'hospital_set':hospitals,'heading':header,'left_button':left_button,'right_button':right_button,'obj_type':obj_type,'action':action,'qs':'' })
def view_physicians_qs(request): 
    obj_type = 'physicianqs'
    action = 'delete'
    left_button = "Uninvite"
    right_button = "Cancel"
    heading = "Uninvite Physician"
    mess = "Upon Deletion the Quick Start Link will become deactive."
    qs=True

    if request.method == 'POST':
        searchTerms = request.POST.get('search','').split()
        if searchTerms:
            for i in range(len(searchTerms)):
                if i == 0:
                    physicians = quickStartPhysician.objects.filter(first_name__icontains=searchTerms[i])
                    print('i-',i,'physician',physicians)
                else:
                    physicians = physicians | quickStartPhysician.objects.filter(first_name__icontains=searchTerms[i])
                physicians = physicians | quickStartPhysician.objects.filter(last_name__icontains=searchTerms[i])
                physicians = physicians | quickStartPhysician.objects.filter(specialty__tag__icontains=searchTerms[i])
                physicians = physicians | quickStartPhysician.objects.filter(email__icontains=searchTerms[i])
                
                print('i-',i,'physician',physicians)
        object_set = list(set(physicians))
        return render(request, template_name='views/physician_list_masteruser.html',context={'qs':qs,'object_set':object_set,'action':action,'obj_type':obj_type,'left_button':left_button,'right_button':right_button,'heading':heading})

    if request.user.is_superuser:
        object_set = quickStartPhysician.objects.all()
    else:
        object_set =  request.user.hospitals.all()[0].qsp.all() | request.user.qs_hospital.qs_physicians.all()
   
    return render(request, template_name='views/physician_list_masteruser.html',context={'qs':qs,'object_set':object_set,'action':action,'obj_type':obj_type,'left_button':left_button,'right_button':right_button,'heading':heading})

def searchViewQuickPhysician(request):
    if request.method == 'POST':
        
        searchTerms = request.POST.get('search','').split()
        if request.user.is_superuser:
            
            for i in range(len(searchTerms)):
                if i == 0:
                    qs_physicians = quickStartPhysician.objects.filter(first_name__icontains=searchTerms[i])
                else:
                    qs_physicians = qs_physicians | quickStartPhysician.objects.filter(first_name__icontains=searchTerms[i])

                qs_physicians = qs_physicians | quickStartPhysician.objects.filter(last_name__icontains=searchTerms[i])
                qs_physicians = qs_physicians | quickStartPhysician.objects.filter(email__icontains=searchTerms[i])
                qs_physicians = qs_physicians | quickStartPhysician.objects.filter(hospital__name__icontains=searchTerms[i])

        else:
            qsp = request.user.hospitals.all()[0].quickstartphysician_set.all()

            for i in range(len(searchTerms)):
                if i == 0:
                    qs_physicians = qsp.filter(first_name__icontains=searchTerms[i])
                else:
                    qs_physicians = qs_physicians | qsp.filter(first_name__icontains=searchTerms[i])

                qs_physicians = qs_physicians | qsp.filter(last_name__icontains=searchTerms[i])
                qs_physicians = qs_physicians | qsp.filter(email__icontains=searchTerms[i])

        qs_physicians = list(set(qs_physicians))
        print("pppppppppp",qs_physicians)
        return render(request=request,template_name='views/physician_list_masteruser.html',context={'object_set':qs_physicians,'hospital_set':''})
    return HttpResponse(f"Error")

@login_required
def view_physicians_staff(request):
    
    physician_set = request.user.hospitals.all()[0].physician_set.all()
    return render(request=request,template_name='views/physician_list_masteruser.html',context={'physician_set':physician_set})


def getQsHospitals(request):
    print('hellllll')
    choice = request.POST.get('choice','')
    print(request.POST,'lllll')
    hospital_set = ''
    print('choice', choice)
    if choice:
        if choice == 'inv':
            print('hello')
            hospital_set = quickStartHospital.objects.filter(is_emailed=True)
        elif choice == 'phy':
            print('hell2')
            hospital_set = quickStartHospital.objects.filter(has_physicians=True)
        elif choice == 'onb':
            print('hell3')
            hospital_set = quickStartHospital.objects.filter(is_registered=True)
        else:
            print('hell4')
            hospital_set = quickStartHospital.objects.filter()

    return render(request=request,template_name='views/quickStartHospital.html',context={'hospital_set':hospital_set})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def view_qs_hospitals(request):
    choices = ['All','Is Invited','Has Physicians','Is Registered','Manually Onboarded']
    hospital_set = ''
    header = "Remove Invited Hospital"
    left_button = "Delete"
    right_button = "Cancel"
    action = 'delete'
    obj_type='qshospital'
    selection = 'All'
    if request.method == 'POST':
        button = request.POST.get('button','')
       
        if button == 'search':
            searchTerms = request.POST.get('search','').split()

            for i in range(len(searchTerms)):
                if i == 0:
                    hospital_set = quickStartHospital.objects.filter(hospital_name__icontains = searchTerms[i])
                   
                else:
                    hospital_set= hospital_set | quickStartHospital.objects.filter(hospital_name__icontains = searchTerms[i])
                   

                
                hospital_set = hospital_set | quickStartHospital.objects.filter(hospital_zip__icontains=searchTerms[i])
              
                hospital_set = hospital_set | quickStartHospital.objects.filter(email__icontains=searchTerms[i])
                
                hospital_set = hospital_set | quickStartHospital.objects.filter(user__email__icontains=searchTerms[i])
                
                quickStarted = True

        else:
            choice = request.POST.get('choice','')
            if choice == 'Is Invited':
                selection = 'Is Invited'
                print('hello')
                hospital_set = quickStartHospital.objects.filter(is_emailed=True)
            elif choice == 'Has Physicians':
                print('hell2')
                selection = 'Has Physicians'
                hospital_set = quickStartHospital.objects.filter(has_physicians=True)
            elif choice == 'Is Onboarded':
                print('hell3')
                selection = 'Is Onboarded'
                hospital_set = quickStartHospital.objects.filter(is_registered=True)
            elif choice == 'All':
                hospital_set = quickStartHospital.objects.filter()
            else:
                hospital_set = Hospital2.objects.filter(is_manual=True)
                return render(request=request,template_name='views/hospital_list_master_user.html',context={'hospital_set':hospital_set,'heading':header,'left_button':left_button,'right_button':right_button,'obj_type':obj_type,'action':action})

        return render(request=request,template_name='views/quickStartHospital.html',context={'hospital_set':hospital_set,'choices':choices,'selection':selection,'heading':header,'left_button':left_button,'right_button':right_button,'obj_type':obj_type,'action':action})

    hospital_set = quickStartHospital.objects.filter(soft_delete=False)
    return render(request=request,template_name='views/quickStartHospital.html',context={'hospital_set':hospital_set,'heading':header,'left_button':left_button,'right_button':right_button,'obj_type':obj_type,'action':action,'choices':choices,'selection':selection})




@login_required
@user_passes_test(lambda u: u.is_superuser)
def view_hospitals(request):
    print('hello')
    hospitals = ''
    searchTerm = ''
    quickStarted = False
    button = ''
    header = "Remove Facility"
    message = "Are you sure you want to remove the Hospital"
    left_button = "Delete"
    right_button = "Cancel"
    action = 'delete'
    obj_type='hospital'

    
    if request.method == 'POST':

        searchTerm = request.POST.get('search','')
        button = request.POST.get('button','')
        searchTerms = searchTerm.split()
        if button == 'onboarded':
            for i in range(len(searchTerms)):
                if i == 0:
                    hospitals = Hospital2.objects.filter(name__icontains = searchTerms[i])
                else:
                    hospitals = hospitals | Hospital2.objects.filter(name__icontains = searchTerms[i])
                
                hospitals = hospitals | Hospital2.objects.filter(zip__icontains=searchTerms[i])
                hospitals = hospitals | Hospital2.objects.filter(city__icontains=searchTerms[i])
                hospitals = hospitals | Hospital2.objects.filter(state__icontains=searchTerms[i])
        else:
            for i in range(len(searchTerms)):
                if i == 0:
                    hospitals = quickStartHospital.objects.filter(hospital_name__icontains = searchTerms[i])
                else:
                    hospitals = hospitals | quickStartHospital.objects.filter(hospital_name__icontains = searchTerms[i])
                
                hospitals = hospitals | quickStartHospital.objects.filter(hospital_zip__icontains=searchTerms[i])
                hospitals = hospitals | quickStartHospital.objects.filter(email__icontains=searchTerms[i])
                hospitals = hospitals | quickStartHospital.objects.filter(user__email__icontains=searchTerms[i])
                quickStarted = True

        hospitals = list(set(hospitals))
        if quickStarted:
            return render(request=request,template_name='views/quickStartHospital.html',context={'hospital_set':hospitals,'button':button,'heading':header,'message':message,'left_button':left_button,'right_button':right_button,'obj_type':obj_type,'action':action})
        return render(request=request,template_name='views/hospital_list_master_user.html',context={'hospital_set':hospitals,'button':button,'heading':header,'message':message,'left_button':left_button,'right_button':right_button,'obj_type':obj_type,'action':action})
    hospitals = Hospital2.objects.filter(soft_delete=False)
    return render(request=request,template_name='views/hospital_list_master_user.html',context={'hospital_set':hospitals,'heading':header,'message':message,'left_button':left_button,'right_button':right_button,'obj_type':obj_type,'action':action})

def view_specialties(request):
    specialty_set = ProductTags.objects.all().order_by('tag')
    products_set = Product.objects.all().order_by('name')
    product_name = ''
    buttonClicked = ''
    specialty = ''
    header = "Remove Specialty"
    message = "Are you sure you want to remove the Hospital"
    left_button = "Delete"
    right_button = "Cancel"
    action = 'delete'
    obj_type = 'specialty'

    if request.method == 'POST':
        product_name= request.POST.get('productID','')
        buttonClicked = request.POST.get('button','')
        if buttonClicked == 'dropdown':
            if product_name == 'all':
                specialty_set = ProductTags.objects.all()
            
            else:
                try:
                    product = Product.objects.get(name=product_name)
                    specialty_set = product.specialties.all()
                except (Product.DoesNotExist,Exception) as error:
                    print(error)
                    messages.error(request,message=f"Please submit again. Error.",extra_tags='warning')
        else:
             
            searchterm = request.POST.get('search','')
            searchTerms = searchterm.split()
            if request.user.is_superuser:
                hospital = Hospital2.objects.filter(name__icontains=searchterm)
                physician_set = hospital[0].physician_set.all() if hospital else ''

            if physician_set:
                for i in range(len(physician_set)):
                    if i == 0:
                        specialty = physician_set[i].specialty_ph.all()
                    else:
                        specialty = specialty| physician_set[i].specialty_ph.all()

            else:
                for i in range(len(searchTerms)):
                    if i == 0:
                        specialty = ProductTags.objects.filter(tag__icontains=searchTerms[i])
                    else:
                        specialty = specialty | ProductTags.objects.filter(tag__icontains=searchTerms[i])
                    specialty = specialty | ProductTags.objects.filter(products__name__icontains=searchTerms[i])
                    specialty = specialty | ProductTags.objects.filter(physicians__firstName__icontains=searchTerms[i])
                    specialty = specialty | ProductTags.objects.filter(physicians__lastName__icontains=searchTerms[i])
            

        return render(request,template_name='views/specialties.html',context={'products_set':products_set,'specialty_set':list(set(specialty)) if specialty else specialty_set,'product_name':product_name,'heading':header,'message':message,'left_button':left_button,'right_button':right_button})
  
        
        
    return render(request,template_name='views/specialties.html',context={'products_set':products_set,'specialty_set':specialty_set,'product_name':product_name,'heading':header,'message':message,'left_button':left_button,'right_button':right_button,'action':action,'obj_type':obj_type})

# ------------------------------------------- Products View ----------------------------------------------------------------------- #


def viewProductList(request):
    product_set = ''
    specialties = ''
    obj_type = 'product'
    action = 'delete'
    left_button = 'Delete'
    right_button = 'Cancel'
    queryset = ''
    next = ''
    previous = ''
    letter = request.GET.get('letter','A').upper()
    if letter == 'A':
        next = ALPHABET[ALPHABET.index(letter) + 1]
    elif letter == 'Z':
        previous = ALPHABET[ALPHABET.index(letter) - 1]
    else:
        try:
            previous = ALPHABET[ALPHABET.index(letter) - 1]
            next = ALPHABET[ALPHABET.index(letter) + 1]
        except ValueError as error:
            print(error)
            previous = ''
            next = 'B'
            messages.error(request,message="There was an error retrieving products. Please contact the administrator for more information.",extra_tags='warning')

        specialty_tag = ''
        
    if request.user.is_superuser:
        print("if requesrt is superuser")
        queryset = ''
        physician_set = ''
        # product_set = Product.objects.filter(soft_delete=False)
        specialties = ProductTags.objects.all()
        product_set = Product.objects.filter(name__istartswith=letter)

        # paginator = Paginator(product_set,per_page=8)
        # page = request.GET.get('page',1)

        # try:
        #     products = paginator.page(page)
        # except PageNotAnInteger as error:
        #     products = paginator.page(1)
        # except EmptyPage as error:
        #     products = paginator.page(paginator.num_pages)

        # alphabet = []
        
    else:
        print("if request is not superuser")
        setProducts = set()
        physician_set = request.user.hospitals.all()[0].physician_set.all()
        #  build query set so search can filter on the proper subset of items belonging to only physicians which are members of their respective hospital
        product_set = set([product for physician in physician_set for product in physician.productitems.all()])
        specialties = list(set([specialty for phys in physician_set for specialty in phys.specialty_ph.all()]))
    # post request can either come from a search button or come from the drop down filter.
    if request.method == 'POST':
        print('cif request is post',request.POST)
        # create queryset to search only if request is not superuser
        specialty_tag = request.POST.get('specialty','')
        button = request.POST.get('button','')
        print('specialty',specialty_tag)
        if button == 'search':
            print('xxxxxxxxxx')
            if physician_set and not request.user.is_superuser:
                queryset = ''
                for i in range(len(physician_set)):
                    if i == 0:
                        queryset = physician_set[i].productitems.all()
                    else:
                        queryset = queryset | physician_set[i].productitems.all()
            print('queryset',queryset,'productset',product_set)
            searchTerms = request.POST.get('searchTerms','')
            if (searchTerms and (queryset or product_set)):
                print("what the fuck cmon")
                print('searchterms',searchTerms)
                print("=" in searchTerms)
                if "=" in searchTerms:
                    print("after equals")
                    product_set = returnSearch(searchTerms=searchTerms,object_set=queryset if queryset else product_set,searchMapping=SEARCHMAPPING["product"])
                else:
    
                    searchTerms = searchTerms.split()
                    print('array',searchTerms)
                    for i in range(len(searchTerms)):
                        if i == 0:
                            product_set = Product.objects.filter(name__icontains=searchTerms[i])
                            print('firstIf',i,product_set)
                            print(" ")

                        else:
                            product_set = product_set | Product.objects.filter(name__icontains=searchTerms[i])
                            print('else',i,product_set)
                        print('afterelse',i,product_set)
                        print(" ")
                        product_set= product_set | Product.objects.filter(specialties__tag__icontains=searchTerms[i])
                        print('afterelse1',i,product_set)
                        print(" ")
                        product_set= product_set | Product.objects.filter(physician__lastName__icontains=searchTerms[i])
                        print('afterelse2',i,product_set)
                        print(" ")
                        product_set= product_set | Product.objects.filter(physician__firstName__icontains=searchTerms[i])
                        print('prodsetbottom3',i,product_set)
                        print(" ")
                    product_set = set(product_set)
                    print('prodsetbottom4',i,product_set)

        else:
            if specialty_tag != 'all':
                try:
                    product_set = ProductTags.objects.get(tag=specialty_tag).products.all()
                except (ProductTags.DoesNotExist,Exception) as error:
                    print(error)
                    return
            #  else product tags will already be sset from above if it is set to all.
            # keep going and break out of the if block and render
            
            
        return render(request,template_name='views/view_products.html',context={'posts':product_set,'specialty_set':specialties,'tag':specialty_tag,'obj_type':obj_type,'action':action,'left_button':left_button,'right_button':right_button,'letter':letter,'alphabet':ALPHABET,'prev':previous,'next':next})

    # if request.is_superuser:
    #     product_set = Product.objects.all()
    # else:
    #     setProducts = set()
    #     physician_set = request.user.hospitals.physician_set.all()
    #     products_set = set([product for physician in physician_set for product in physician.productitems.all()])
    #     specialties = list(set([(specialty.id, specialty.tag) for phys in physician_set for specialty in phys.specialty_ph.all()]))
    
    return render(request,template_name='views/view_products.html',context={'posts':product_set,'specialty_set':specialties,'obj_type':obj_type,'action':action,'left_button': left_button, 'right_button':right_button,'alphabet':ALPHABET,'letter':letter,'prev':previous,'next':next})
# @login_required
# def viewProductList(request):
#     product_set = ''
#     specialties = ''
#     obj_type = 'product'
#     action = 'delete'
#     left_button = 'Delete'
#     right_button = 'Cancel'
#     queryset = ''
#     if request.user.is_superuser:
#         print("if requesrt is superuser")
#         queryset = ''
#         physician_set = ''
#         product_set = Product.objects.filter(soft_delete=False)
#         specialties = ProductTags.objects.all()

#         # paginator = Paginator(product_set,per_page=8)
#         # page = request.GET.get('page',1)

#         # try:
#         #     products = paginator.page(page)
#         # except PageNotAnInteger as error:
#         #     products = paginator.page(1)
#         # except EmptyPage as error:
#         #     products = paginator.page(paginator.num_pages)

        
        
#     else:
#         print("if request is not superuser")
#         setProducts = set()
#         physician_set = request.user.hospitals.all()[0].physician_set.all()
#         #  build query set so search can filter on the proper subset of items belonging to only physicians which are members of their respective hospital
#         product_set = set([product for physician in physician_set for product in physician.productitems.all()])
#         specialties = list(set([specialty for phys in physician_set for specialty in phys.specialty_ph.all()]))
#     # post request can either come from a search button or come from the drop down filter.
#     if request.method == 'POST':
#         print('cif request is post',request.POST)
#         # create queryset to search only if request is not superuser
#         specialty_tag = request.POST.get('specialty','')
#         button = request.POST.get('button','')
#         print('specialty',specialty_tag)
#         if button == 'search':
#             print('xxxxxxxxxx')
#             if physician_set and not request.user.is_superuser:
#                 queryset = ''
#                 for i in range(len(physician_set)):
#                     if i == 0:
#                         queryset = physician_set[i].productitems.all()
#                     else:
#                         queryset = queryset | physician_set[i].productitems.all()
#             print('queryset',queryset,'productset',product_set)
#             searchTerms = request.POST.get('searchTerms','')
#             if (searchTerms and (queryset or product_set)):
#                 print("what the fuck cmon")
#                 print('searchterms',searchTerms)
#                 print("=" in searchTerms)
#                 if "=" in searchTerms:
#                     print("after equals")
#                     product_set = returnSearch(searchTerms=searchTerms,object_set=queryset if queryset else product_set,searchMapping=SEARCHMAPPING["product"])
#                 else:
    
#                     searchTerms = searchTerms.split()
#                     print('array',searchTerms)
#                     for i in range(len(searchTerms)):
#                         if i == 0:
#                             product_set = Product.objects.filter(name__icontains=searchTerms[i])
#                             print('firstIf',i,product_set)
#                             print()

#                         else:
#                             product_set = product_set | Product.objects.filter(name__icontains=searchTerms[i])
#                             print('else',i,product_set)
#                         print('afterelse',i,product_set)
#                         print()
#                         product_set= product_set | Product.objects.filter(specialties__tag__icontains=searchTerms[i])
#                         print('afterelse1',i,product_set)
                        
#                         product_set= product_set | Product.objects.filter(physician__lastName__icontains=searchTerms[i])
#                         print('afterelse2',i,product_set)
#                         product_set= product_set | Product.objects.filter(physician__firstName__icontains=searchTerms[i])
#                         print('prodsetbottom3',i,product_set)
#                     product_set = set(product_set)

#         else:
#             if specialty_tag != 'all':
#                 try:
#                     product_set = ProductTags.objects.get(tag=specialty_tag).products.all()
#                 except (ProductTags.DoesNotExist,Exception) as error:
#                     print(error)
#                     return
#             #  else product tags will already be sset from above if it is set to all.
#             # keep going and break out of the if block and render
            
            
#         return render(request,template_name='views/view_products.html',context={'products_set':product_set,'specialty_set':specialties,'tag':specialty_tag,'obj_type':obj_type,'action':action,'left_button':left_button,'right_button':right_button})

#     # if request.is_superuser:
#     #     product_set = Product.objects.all()
#     # else:
#     #     setProducts = set()
#     #     physician_set = request.user.hospitals.physician_set.all()
#     #     products_set = set([product for physician in physician_set for product in physician.productitems.all()])
#     #     specialties = list(set([(specialty.id, specialty.tag) for phys in physician_set for specialty in phys.specialty_ph.all()]))
    
#     return render(request,template_name='views/view_products.html',context={'posts':products,'specialty_set':specialties,'obj_type':obj_type,'action':action,'left_button': left_button, 'right_button':right_button})


@login_required
def view_products(request):
    hospitals = ''
    opacity = "1.0"
    if request.user.is_superuser:
        physicians = Physician.objects.all()
        hospitals = Hospital2.objects.all()
        print(hospitals)
    else:
        physicians = Physician.objects.filter(facility=request.user.hospitals.first())
    specialties = ProductTags.objects.all()
    if request.user.is_superuser:
        return render(request, template_name='views/p2.html',context={'physicians':physicians,'specialties':specialties,'hospitals':hospitals})
    else:
        return render(request, template_name='views/p2.html',context={'physicians':physicians,'specialties':specialties,'hospitals':[]})


def toggleAllorCurrent(request):
    print('ppppp')
    productTagProducts = ''
    buildAll = False
    physician = request.POST.get('physician','')
    specialty = request.POST.get('specialty','')

    try:
        specialty = specialty
        specialties = ProductTags.objects.get(tag=specialty)
        products = specialties.products.all()
        buildAll = True
        physician = int(physician)
        physician_model = Physician.objects.get(id=physician)
    except (ProductTags.DoesNotExist,Exception) as error:
        print(error)
    else:
        productTagProducts = [( model_to_dict(prod), prod.getPictureURL(), prod.buildSpecialtiesString(), True if prod in physician_model.productitems.all() else False )  for prod in products]

        for product in productTagProducts:
            product[0].pop('picture')
            product[0].pop('created_at')
    print(productTagProducts)
    return JsonResponse(data={'dataset':productTagProducts,'buildAll':buildAll})

def buildProductCards1(request):
    productTagProducts = ''
    productTagProducts1 = ''
    buildAllTab = ''
    model = ''
    products = ''
    physician = request.POST.get('physician','')
    hospital = request.POST.get('hospital','')
    specialty = request.POST.get('specialty','')
    buildSpecial = False

    print('specccc',specialty)
    
    if specialty:
        try:
            specialty_model = ProductTags.objects.get(tag=specialty)
        except (ProductTags.DoesNotExist,Exception) as error:
            print(error)

        if hospital and physician:
            print('here2')

        elif hospital:
            print('here3')
            hospital = int(hospital)
            try:
                hospital_model = Hospital2.objects.get(id=hospital)
            except (Hospital2.DoesNotExist,Exception):
                print(error)
            else:
                physician_set = hospital_model.physician_set.all()
                product_array_set = set()
            
                for physician_ in physician_set:
                    prods = physician_.productitems.all() if specialty == 'all' else physician_.productitems.filter(specialties__tag__in=[specialty])
                    print("prods",prods)
                    for prod in prods:
                        product_tuple = (prod, prod.getPictureURL() ,prod.buildSpecialtiesString() )
                    
                    
                        product_array_set.add(product_tuple)
            
                productTagProducts = [(model_to_dict(prodTup[0]),prodTup[1],prodTup[2])  for prodTup in product_array_set ]
                buildSpecial = True
            
        elif physician:
            print('here4')
            buildAllTab = True
            try:
                if physician == 'all':
                    if specialty == 'all':
                        products = Product.objects.all()
                    else:
                        products = specialty_model.products.all()
                else:
                    print('came hereeenjqwene')
                    try:
                        physician = int(physician)
                        model = Physician.objects.get(id=physician)
                        
                    except (Physician.DoesNotExist,Exception) as error:
                        print(error)
                        return
                    buildSpecial = True
                    print('here8')
                    if specialty == 'all':
                        
                        print('here9')
                        prods = Product.objects.all()
                        productTagProducts = [(model_to_dict(prod),prod.getPictureURL(),specialty,True if prod in model.productitems.all() else False) for prod in prods]
                        print('24',productTagProducts1)
                        productTagProducts1 = [(model_to_dict(Product.objects.get(id=prod['id'])),Product.objects.get(id=prod['id']).getPictureURL(),key,True) for key,value in model.products.items() for prod in value]
                        # buildSpecial = True
                    else:
                        prods = model.productitems.all()
                        print('here10')
                        productTagProducts = [(model_to_dict(prod),prod.getPictureURL(),specialty) for prod in prods]
                        print('24',productTagProducts1)
                        products = model.linkedtags.filter(tag=specialty)[0].products.all()

            except (Physician.DoesNotExist,Exception) as error:
                print(error)
                return HttpResponse(f"Error-{error}")
            
        else:
            print('here5')

            if specialty == 'all':
                try:
                    products = Product.objects.all()
                except (Product.DoesNotExist,Exception) as error:
                    print(error)
                

            else:
                try:
                    
                    model = ProductTags.objects.get(tag=specialty)
                    products = model.products.all()
                    
                except (ProductTags.DoesNotExist,Exception) as error:
                    print(error)

        if not buildSpecial:
            productTagProducts = [( model_to_dict(prod), prod.getPictureURL(), prod.buildSpecialtiesString() )  for prod in products]
        for product in productTagProducts:
                    
                    product[0].pop('picture')
                    product[0].pop('created_at')
        print(productTagProducts)
        print("did it come here")
        return JsonResponse(data={'dataset':productTagProducts,'buildAll':buildAllTab})
        
        
    
@login_required
@user_passes_test(lambda u: u.is_superuser)
def filterPhysicians(request):

    if request.method == 'POST':
        print("where")
        facility_id = request.POST.get('facility', '')
        print(facility_id)
        # specialty_name = request.POST.get('specialty', '')
        # physician_id = request.POST.get('physician', '')
        # specialties = ''
        # if (facility_id):
        #     try:
        #         facility_id = int(facility_id)
        #         hospital = Hospital2.objects.get(id=facility_id)
        #         physician_set = hospital.physician_set.all()

        #         physicians = list(hospital.physician_set.all().values_list('id','firstName','lastName'))

        #     except (Hospital2.DoesNotExist,Exception,IndexError) as error:
        #         print(error)
        #     else:
        #         if (physician_id == 'all'):


        if facility_id:
            
            try:
                facility_id = int(facility_id)
                hospital = Hospital2.objects.get(id=facility_id)
                physician_set = hospital.physician_set.all()
                physicians = list(hospital.physician_set.all().values_list('id','firstName','lastName'))
            except (Hospital2.DoesNotExist,Exception) as HDNE:
                return JsonResponse(data={'dataset':HDNE})
            else:
                specialties = list(set([(specialty.id, specialty.tag) for phys in physician_set for specialty in phys.specialty_ph.all()]))
                print(specialties)

                
            # else:
            #     print("testing")
            #     return JsonResponse(data={'dataset': physicians})
            # return JsonResponse(data={'dataset':[1,2,3]})

        else:
            try:
                physicians = list(Physician.objects.all()[0:30].values_list('id','firstName','lastName'))
                print('helllooo bitch')
                specialties = list(ProductTags.objects.all().values_list('id','tag'))
            except Exception as error:
                print(error)
    
        return JsonResponse(data={'dataset': physicians,'specialties':specialties})   
    
# def view_products(request):
#     return render(request,template_name='views/products.html',context={})
def filterSpecialties(request):
    physician_id = request.POST.get('physician','')
    specialties = ''
    print("hello")

    if not physician_id:
        try:
                physicians = list(Physician.objects.all()[0:30].values_list('id','firstName','lastName'))
                specialties = list(ProductTags.objects.all().values_list('id','tag'))
        except Exception as error:
            print(error)
            

    elif physician_id:
        if physician_id == 'all':
            specialties = list(ProductTags.objects.all().values_list('id','tag'))
        else:
            try:
                physician = Physician.objects.get(id=physician_id)
                specialties = list(physician.specialty_ph.all().values_list('id','tag'))
            except (Physician.DoesNotExist,Exception) as error:
                print(error)
    
    return JsonResponse(data={'dataset':specialties})
        
  
def buildProductCards(request):
    productTagProducts = ''
    buildAllTab = ''
    model = ''
    products = ''
    print("reue,POST",request.POST)
    physician = request.POST.get('physician','')
    hospital = request.POST.get('hospital','')
    specialty = request.POST.get('specialty','')
    print('reww',request.POST)
    buildSpecial = False

    print('specccc',specialty)
    
    if specialty:

        try:
            specialty_model = ProductTags.objects.get(tag=specialty)
        except (ProductTags.DoesNotExist,Exception) as error:

            print(error)
        print()
        if hospital and physician:
            print('here2')

        if hospital and not physician:
            print('here3')
            hospital = int(hospital)
            try:
                hospital_model = Hospital2.objects.get(id=hospital)
            except (Hospital2.DoesNotExist,Exception):
                print(error)
            else:
                physician_set = hospital_model.physician_set.all()
                product_array_set = set()
            
                for physician_ in physician_set:
                    prods = physician_.productitems.all() if specialty == 'all' else physician_.productitems.filter(specialties__tag__in=[specialty])
                    print("prods",prods)
                    for prod in prods:
                        product_tuple = (prod, prod.getFirstImage() ,prod.buildSpecialtiesString() )
                        product_array_set.add(product_tuple)
                print(product_array_set)
                productTagProducts = [(model_to_dict(prodTup[0]),prodTup[1],prodTup[2],'')  for prodTup in product_array_set ]
                buildSpecial = True
        elif physician:
            print('here4')
            buildAllTab = True
            try:
                if physician == 'all':
                    if specialty == 'all':
                        products = Product.objects.all()
                    else:
                        products = specialty_model.products.all()
                else:
                    buildSpecial = True
                    try:
                        print('cme here4 inside')
                        physician = int(physician)
                        print('cme here4 inside2')
                        model = Physician.objects.get(id=physician)
                        print(model)
                        print('cme here4 inside3')
                    except (Physician.DoesNotExist,Exception) as error:
                        ("wht the mother fcking fck")
                        print(error)
                        return
                    if specialty == 'all':
                        products = model.productitems.all()
                    else:
                        print(specialty,'specilty')
                        products = specialty_model.products.all()
                        # products = set(model.productitems.all()) | set(products).difference(set(model.productitems.all()))
                        # print(products)

                    productTagProducts = [( model_to_dict(prod), prod.getFirstImage(), prod.buildSpecialtiesString(), True if prod in model.productitems.all() else False )  for prod in products]
                    print(productTagProducts,'ppppyyyttttrr')
                    temp = []
                    for product in productTagProducts.copy():
                        if product[3]:
                            temp.append(product)
                            productTagProducts.remove(product)
                    temp.extend(productTagProducts)
                    productTagProducts = temp
                        
                    




            except (Physician.DoesNotExist,Exception) as error:
                ("wht the mother fcking fck")
                print(error)
                return HttpResponse(f"Error-{error}")
            
        else:
            print('here5')

            if specialty == 'all':
                try:
                    products = Product.objects.all()
                except (Product.DoesNotExist,Exception) as error:
                    ("wht the mother fcking fck2")
                    print(error)
            else:
                try:
                    print('here5',specialty)
                    model = ProductTags.objects.get(tag=specialty)
                    products = model.products.all()
                    
                except (ProductTags.DoesNotExist,Exception) as error:
                    ("wht the mother fcking fck3")
                    print(error)

        if not buildSpecial:
            productTagProducts = [( model_to_dict(prod), prod.getFirstImage(), prod.buildSpecialtiesString(),'' )  for prod in products]
        for product in productTagProducts:
                    
                    product[0].pop('picture')
                    product[0].pop('created_at')
        # print(productTagProducts)
        # for p in productTagProducts:
        #     print(p)
        #     print()
        #     print()
        return JsonResponse(data={'dataset':productTagProducts,'buildAll':buildAllTab})

# ------------------------------------------- Products View END----------------------------------------------------------------------- #

@login_required
@user_passes_test(lambda u: u.is_superuser)
def view_recent_activity(request):
    return HttpResponse(content="Activity Log View Coming Soon")

@login_required
@user_passes_test(lambda u: u.is_superuser)
def invite_hospital_view(request):
    # Grabbing the hospitals to display in the invite_hospital_view. Both onboarded and quickstarted hospitals.
    recently_invited_hositals = quickStartHospital.objects.all().order_by('created_at__second')[0:5]
    hospitals = Hospital2.objects.all().order_by('created_at__second')[0:5]
    header = "Registration is not completed"
    message = "Please Send Reminder To Hospital User OR Complete Registration Yourself!"
    left_button = "Send Reminder"
    right_button = "Complete Yourself"
    # form for sending the quick invite to hospital.
    if request.method == 'POST':
        
        form = QuickStartHospitalInvite(request.POST)
        if form.is_valid():
           
            print("came here")
            try:
                qs_hospital = form.save()
                link = buildJWTQuickStartHospital(qs_hospital=qs_hospital, domain=request.META.get('HTTP_HOST', ''))
                message = f"Thank You for Signing Up. Please visit the secure link to Quick start hospital. {link}"
                if qs_hospital.email:
                    send_msg_email(message=message,to=qs_hospital.email,previousURL=request.META.get('HTTP_REFERER'))
                else:
                    send_msg_email(message=message,previousURL=request.META.get('HTTP_REFERER'))


            except (SMTPExc) as smtp:
                messages.error(request=request,message=f"There was an error sending an invite email to {qs_hospital.hospital_name}.",extra_tags='warning')
                return HttpResponse(f"{smtp}")
            except (Exception) as error:
                messages.error(request=request,message=f"An exception occurred while processing your request. Please try again or contact the administrator if the problem persists.",extra_tags='warning')
                return HttpResponse(f"{error}")
            try:
                qsl = QuickInviteLogs(email=qs_hospital.email,entity_type="hospital",entity_name=qs_hospital.hospital_name,message=0,action="Quick Invite(Hospital)")
                qsl.user = request.user
                qsl.save()
            except Exception as error:
                print(error)

            qs_hospital.is_emailed = True
            qs_hospital.number_emails_sent += 1
            qs_hospital.save()
            return render(request=request,template_name='register/invite_hospital_send_message.html',context={'qs_hospital':qs_hospital})
        print(form.errors)
        return render(request=request,template_name='views/invite_hospital1.html',context={'recently_invited_hospitals':recently_invited_hositals,'hospitals':hospitals,'form':form})
    # 'heading':header,'message':message,'left_button':left_button,'right_button':right_button
    
    form = QuickStartHospitalInvite()
    return render(request=request,template_name='views/invite_hospital1.html',context={'recently_invited_hospitals':recently_invited_hositals,'hospitals':hospitals,'form':form})
                #  'heading':header,'message':message,'left_button':left_button,'right_button':right_button}



# def invite_physician_view(request):
#     header = "Quick Start Physician"
#     invite = "Send Invite"
#     if request.method == 'POST':
#         form = QuickStartPhysicianForm(data = request.POST)
#         if form.is_valid():
#             qs_physician = form.save(commit=True)
#             # craft JWT Link to send
#             try:
#                 link = buildJWTQuickStartPhysician(qs_physician=qs_physician)
#                 message = f"Please copy and paste the following secure link in your browser to quickstart. {link}"
#                 send_msg_email(message=message)
#             except (SMTPExc) as smtp:
#                 messages.error(request=request,message=f"There was an error sending an invite email to {qs_physician.first_name} {qs_physician.last_name}")
#                 return HttpResponse(f"{smtp}")
#             except (Exception) as error:
#                 messages.error(request=request,message=f"An exception occurred while processing your request. Please try again or contact the administrator if the problem persists.")
#                 return HttpResponse(f"{error}")
            
#             messages.success(request=request,message=f"Succesfully sent an invite to Physician: {qs_physician.first_name} {qs_physician.last_name}")
#             return HttpResponseRedirect(reverse('dashboard:master_dashboard'))
        
#         return render(request=request, template_name='views/invite_physician.html', context={'form':form,'header':header,'button':invite})

#     form = QuickStartPhysicianForm()
#     return render(request=request, template_name='views/invite_physician.html', context={'form':form,'header':header,'button':invite})

def filterPhysicians(request):
    if request.method == 'POST':
        hospital_id = request.POST.get('hospital_id','')
        try:
            if hospital_id == 'all':
                physician_set = Physician.objects.all().order_by('facility__name')
            else:
                hospital = Hospital2.objects.get(id=hospital_id)
                physician_set = hospital.physician_set.all().order_by('lastName')
        except (Hospital2.DoesNotExist,Exception) as error:
            print(error)
            return HttpResponse(content="Error while submitting request.")
        physicians = [ {'picture':physician.picture.url,'hospital':physician.facility.name, 'name': physician.get_full_name(), 'tags': ", ".join(list(physician.products.keys())) }  for physician in physician_set ]
        return JsonResponse(data={'dataset':physicians})
        
def t1(request):
    form =QuickStartPhysicianForm()
    return render(request,template_name="quickstart/quickstartphysician.html",context={'form':form})

def congrats(request):
    return render(request=request,template_name='register/invite_hospital_send_message.html',context={})
def sendReminderPhysician(request,id):
    try:
        qs_physician = quickStartPhysician.objects.get(id=id)
        link,hospital_name = buildJWTQuickStartPhysician(qs_physician= qs_physician)
        message = f"Thank You for Signing Up. Please visit the secure link to quick start hospital. {link}"
        send_msg_email(message=message,to="specialreminder@gmail.com")
    except (quickStartHospital.DoesNotExist, Exception) as error:
        messages.error(request,message=f"There was an error processing your request. Please try again later or submit a reminder manually.",extra_tags='warning')
    else:
        messages.success(request,message=f"Reminder Email sent to {qs_physician.get_full_name} @ {hospital_name}",extra_tags='success')
        qsl = QuickInviteLogs(email=qs_physician.email,entity_name=hospital_name,entity_type="qsphysician",message=0,action="Invite Reminder(Physician)")
        qsl.user = request.user
        qsl.save()
    return HttpResponseRedirect(reverse('views:view_physicians_qs'))

def sendReminderHospital(request,id):
    try:
        qs_hospital = quickStartHospital.objects.get(id=id)
        link = buildJWTQuickStartHospital(qs_hospital=qs_hospital)
        message = f"Thank You for Signing Up. Please visit the secure link to quick start hospital. {link}"
        send_msg_email(message=message,to="specialreminder@gmail.com")
    except (quickStartHospital.DoesNotExist, Exception) as error:
        messages.error(request,message=f"There was an error processing your request. Please try again later or submit a reminder manually.",extra_tags='warning')
    else:
        qsl = QuickInviteLogs(email=qs_hospital.email,entity_name=qs_hospital.hospital_name,entity_type="qshospital",message=0,action="Invite Reminder(Hospital)")
        qsl.user = request.user
        qsl.save()
        messages.success(request,message=f"Reminder Email sent to {qs_hospital.hospital_name} @ {qs_hospital.email}",extra_tags='success')
    return HttpResponseRedirect(reverse('views:invite_hospital_view'))

def sendReminderManual(request,id):

    return HttpResponse("WHAT THE FUCK DO I DO")

# def quickStartHosital(request):

#     if request.method == 'POST':
#         form = QuickStartHospitalInvite(request.POST)
#         if form.is_valid():
#             qs_hospital = form.save()
#             try:
#                 link = buildJWTQuickStartHospital(qs_hospital=qs_hospital)
#                 message = f"Thank You for Signing Up. Please visit the secure link to quick start hospital. {link}"
#                 send_msg_email(message=message)
#             except (SMTPExc) as smtp:
#                 messages.error(request=request,message=f"There was an error sending an invite email to {qs_hospital.hospital_name}.")
#                 return HttpResponse(f"{smtp}")
#             except (Exception) as error:
#                 messages.error(request=request,message=f"An exception occurred while processing your request. Please try again or contact the administrator if the problem persists.")
#                 return HttpResponse(f"{error}")
#             messages.success(request=request,message=f"Succesfully sent an invite to Name: {qs_hospital.hospital_name} @ Email: {qs_hospital.email}")
#             return HttpResponseRedirect(reverse('medical:dashboard'))

#         return render(request,template_name='quickstart/quickStartHospital.html', context={'form':form})
            
#     form = QuickStartHospitalInvite()
#     return render(request,template_name='quickstart/quickStartHospital.html', context={'form':form})

def physician_detail_view(request,id):

    try:
        physician = Physician.objects.get(id=id)
    except (Physician.DoesNotExist,Exception) as error:
        return HttpResponse(f"this is the error {error}")
    
    return render(request, template_name='views/recommended_products_listed.html',context={'physician':physician})



# def filterPhysiciansListView(request):

#     facility_id = request.POST.get('hospital_id',0)

#     print(facility_id)
    
#     try:
#         if facility_id == 'all':
#             physicians = Physician.objects.all()

#         else:
#             facility_id = int(facility_id)
#             hospital = Hospital2.objects.get(id=facility_id)
#             print(hospital)
#             physicians = hospital.physician_set.all()
#         print("fuckuuuuuu")
        
#         physician_set = [( model_to_dict(physician), physician.returnPictureURL(), physician.buildSpecialtyString(),physician.facility.name )  for physician in physicians]
#         print(physician_set)
       
#         for physician in physician_set:
                        
#             physician[0].pop('picture')
#             physician[0].pop('created_at')
#             physician[0].pop('updated_at')
#             physician[0].pop('productitems')
#         print("whatthefuck")
#         return JsonResponse(data={'dataset':physician_set})
#     except (Exception) as error:
#         print("whattttt")
#     return JsonResponse(data={'dataset':physician_set})
            