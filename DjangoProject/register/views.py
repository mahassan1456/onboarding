from django.shortcuts import render
from .forms import AddHospitalForm, Login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout as logout_user
from django.contrib.auth import login as login_user
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate, logout as logout_user
from django.forms.models import model_to_dict 
from django.contrib.auth.models import User 
from medical.models import Hospital2 as Hospitals
from medical.forms import AddHospital
from pproducts.models import Physician,ProductTags,Product
from .forms import EditPhysician
from pproducts.forms import AddPhysicianAdmin,AddProducts, AddProductTags
from django.forms.models import model_to_dict
from django.db import IntegrityError
from quickstart.models import quickStartHospital1,quickStartPhysician
from superuseractions.models import UserHistoryTable



# hThis is another comment to test git functionality

# Users who do NOT register with an invite link can also register from here. APPROVAL PROCESS???
# @login_required
# @user_passes_test(lambda u: u.is_superuser)
def register(request):
    qs = request.GET.get('qs','')
    id = request.GET.get('qsid','')
    if qs:
        try:
            qs_hospital = quickStartHospital1.objects.get(id=id)
        except (quickStartHospital1.DoesNotExist,Exception) as error:
            print(error)
    if request.method == 'POST':
        form = AddHospitalForm(request.POST,request.FILES)
        if form.is_valid():
            print(request.POST,'rqqqqqqqq')
            hospital = form.save()
            print('hps',hospital.is_manual)
            if hospital:
                hospital.logRecord(action="1",action_verbose = " Account for ")

                # uht = UserHistoryTable.objects.create(action="1",entity_type="Hospital",entity_id=hospital.id,entity_name=hospital.name,action_verbose=" Account for ",page_link=f"/register/edit/hospital/{hospital.id}/")
                # uht.user = request.user
                # uht.save()
                # request.user.save()
            if request.user.is_superuser:
                messages.success(request,message=f"Succesfully created Hospital {hospital.name.title()}",extra_tags='success')
                return HttpResponseRedirect(reverse('dashboard:master_dashboard'))
            return render(request=request,template_name='register/account_created.html',context={'hospital':hospital})
        return render(request,template_name='register/registration_.html',context={'form':form})
    if qs:
        form = AddHospitalForm(initial={'is_manual':True,'prompt_credentials':True,'name':qs_hospital.hospital_name,'email':qs_hospital.email,'phone': qs_hospital.phone})
    else:
        form = AddHospitalForm(initial={'is_manual':True,'prompt_credentials':True})
    return render(request,template_name='register/registration_.html',context={'form':form})


def registerManual(request,id):
    try:
        qs_hospital = quickStartHospital1.objects.get(id=id)
    except (quickStartHospital1.DoesNotExist,Exception) as error:
        print(error)
        return
    


def accountConfirm(request):
    return render(request,template_name='register/test.html',context={})


    return render(request,template_name='register/account_created.html',context={})

def createCredentials(request,id):
    print('hello world')
    try:
        admin = User.objects.get(id=id)
        
    except (Hospitals.DoesNotExist,Exception) as error:
        return HttpResponse(content=f"{error}")
    if request.method == 'POST':
        print('came here')
        password = request.POST.get('password','')
        password1 = request.POST.get('password1','')
        if password == password1 and admin:
            admin.set_password(password)
            # return HttpResponse(f"{admin.userprofileadmin.prompt_credentials}----{admin.userprofileadmin.prompt_credentials}--Password-{password}")
            admin.save()
            if admin.userprofileadmin.prompt_credentials:
                print('here dumb ass bitch')
                hospital = admin.hospitals.all()[0]
                hospital.is_manual = False
                admin.userprofileadmin.prompt_credentials = False
                admin.userprofileadmin.save()
                hospital.save()
                admin.save()
                messages.success(request, f"Succesfully Updated Password",extra_tags='success')
                return HttpResponseRedirect(reverse('dashboard:dashboard'))

            messages.success(request,f"Successfully created account for {admin.get_full_name()} at hospital {admin.hospitals.all()[0].name}.",extra_tags='success')
            url = reverse('register:login') + '?account=new'
            return HttpResponseRedirect(url)
        messages.error(request,message=f"There was an error processing your request. Please try again later. If the problem persists pleae contact the administrator at XXXX@XXX.com",extra_tags='warning')
    return render(request=request,template_name='register/login_credentials.html',context={'admin':admin})


# ___________________LogIn page for All Users________________
def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return HttpResponseRedirect(reverse('dashboard:master_dashboard'))
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    new_account = request.GET.get('account','')
    display = 'none'
    if new_account:
        display = 'block'
    if request.method == 'POST':
        form = Login(request.POST)
        print("request",request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username','').lower()
            password = form.cleaned_data.get('password','')

            user = authenticate(request,username=username,password=password)

            if user is not None:
                try:
                    login_user(request=request,user=user)
                except (Exception) as error:
                    print(f"{error}")
                    messages.error(request=request,message=f"error loggin in user",extra_tags='warning')
                    return render(request,template_name='register/login.html',context={'form':form,'display':display})
                
                else:
                    if user.userprofileadmin.prompt_credentials:
                        return HttpResponseRedirect(reverse('register:createCredentials', args=(user.id,)))
                url = request.GET.get('next', '')
                if user.is_superuser:
                    return HttpResponseRedirect(reverse('dashboard:master_dashboard'))
                return HttpResponseRedirect(url if url else reverse('dashboard:dashboard'))
            messages.error(request=request,message=f"Incorrect Pssword",extra_tags='warning')
        return render(request,template_name='register/login.html',context={'form':form,'display':display})
    form = Login()
    return render(request,template_name='register/login.html',context={'form':form,'display':display})

def logout(request):

    logout_user(request)
    return HttpResponseRedirect(reverse('register:login'))

#  END


# EDIT VIEWS
@login_required
def editHospital(request,id):

   
  
    if not request.user.is_superuser:
        if id != request.user.hospitals.all()[0].id:
            return HttpResponse(content=f"You can only edit hospital details for your Home Hospital")
    try:
        onboarded_hospital = Hospitals.objects.get(id=id)
        pictureURL = onboarded_hospital.picture.url if onboarded_hospital.picture else ""
    except (Hospitals.DoesNotExist,Exception) as error:
        print(error)
        return HttpResponse(f"This is an error {error}")
    if request.method == 'POST':
        form = AddHospital(request.POST,request.FILES,instance=onboarded_hospital)
        if form.is_valid():
            hospital = form.save()
            stateCheck = hospital.checkState(data_s=form.changed_data,object_dict=model_to_dict(onboarded_hospital))

            if stateCheck:
                print('what the fuck')
                uht = UserHistoryTable.objects.create(action="2",entity_type="Hospital",entity_id=hospital.id,entity_name=hospital.name,page_link=f"/register/edit/hospital/{hospital.id}/",action_verbose=" Account for ",action_obj=stateCheck)
                print("after the fuck")
                uht.user = request.user
                print("after the fuck234")
                uht.save()
                request.user.save()
            messages.success(request,f"You have succesfully edited the hospital {onboarded_hospital.name}")
            if request.user.is_superuser:
                return HttpResponseRedirect(reverse('dashboard:master_dashboard'))
            else:
                return HttpResponseRedirect(reverse('dashboard:dashboard'))
        print(form.errors)
        return render(request,template_name='register/edit/edit_hospital.html',context={'form':form,'pictureURL':pictureURL})
    form = AddHospital(instance=onboarded_hospital)
    return render(request,template_name='register/edit/edit_hospital.html',context={'form':form,'pictureURL':pictureURL})

@login_required
def editPhysician(request,id):
    lpt=''
    state = {}
    action = ''
    request_type = 'edit'
    # If True, this Flag will tell the edit physician template to display entire list of editable fields including products.
    showAll = request.GET.get('showAll','')
    # Pull 'All' tags from the database in order to build Specialties Checkbox Selections.  If Tag is present in physicians specialty selections then checkbox should be checked.
    # 
    tags = ProductTags.objects.all().order_by('tag')
    try:
        # Pull physician object whose information is going to be edited.
        physician = Physician.objects.get(id=id)
        # Pull a list of tags in a python list to check for inclusion. Data Structure - ['Anterior Hip', 'Back','Foot']
        current_tags = [tag[0].title() for tag in physician.linkedtags.all().values_list('tag')]
        print('current_tags',current_tags)
        # Convert physician object to python dictionary
        dict_physician = model_to_dict(physician)
    except (Physician.DoesNotExist,Exception) as error:
        print(error)
        return HttpResponse(f"This is an error {error}")
    if request.method == 'POST':
        # Build Form with post dictionary and edited physician
        form = EditPhysician(request.POST,request.FILES,instance=physician)
        print('fucccccckkkk bniiiiiia')
        if form.is_valid():
            print("passssses through to is valiud",request.POST)
            physician = form.save()
            created,products = physician.buildProductsSet(data=request.POST)

            state = physician.checkState()
        
            print('products',products)
           
            # changed_data_string = ", ".join([ f"Changed {data} to {getattr(physician,data)}"   for data in form.changed_data if data != 'about_me'])
            if form.changed_data:
                state["delta_profile"] = 'Profile'
                string = f""
                for data in form.changed_data:
                    if data != 'about_me':
                        string = f"{string} {data} Prev: {dict_physician[data]} / Curr: {getattr(physician,data)}"
                state["profile"] = string
            if state:
                print(state)
                action = '2'
                record = UserHistoryTable.objects.create(action='2',change_type="physician",action_obj=state,entity_type='Physician',entity_id=physician.id,entity_name=physician.get_full_name())
                record.user = request.user
                record.save()
                request.user.save()
                messages.success(request, f"Succesfully Updated Physician.",extra_tags='success')
            
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        print(form.errors)
        return render(request,template_name='register/edit/edit_physician_.html',context={'physician':physician,'tags':tags,'form':form,'current_tags':current_tags,'show_all':showAll})
    # tags_list = []
    # for tag in tags:
    #     if tag.tag in current_tags:
    #         tags_list
    #     else:
    #         print(tag.tag)
    form = EditPhysician(instance=physician)
    # return render(request,template_name='register/edit/edit_physician.html',context={'physician':physician,'tags':tags,'form':form})
    return render(request,template_name='register/edit/edit_physician_.html',context={'physician':physician,'tags':tags,'form':form,'current_tags':current_tags,'show_all':showAll})



def getProductDetails(request):
    dataset = ''
    if request.method == 'POST':
        product_id = request.POST.get('product','')
        try:
            product = Product.objects.get(id=int(product_id))
        except (Product.DoesNotExist,Exception) as error:
            print(error)
            return

    return JsonResponse(data={'dataset':dataset})


def fucku(request):
    pass
@login_required
@user_passes_test(lambda u: u.is_superuser)
def editProduct(request,id):
    edit=True
    try:
        product = Product.objects.get(id=id)
        product_dict = model_to_dict(product)
    except (Product.DoesNotExist,Exception) as error:
        print(error)
        return HttpResponse(f"{error}")
    
    if request.method == 'POST':
        print('vjdnfewjkfnwejkfnwjkefnwjrefnerjkgnferkjgnerkjgnertjkgnrtjkgnrjgnrtjgknrtjkgnrtjgknrtjkgnrtjkgnrtjkgnrt')
        form = AddProducts(request.POST,request.FILES,instance=product)
        if form.is_valid():
            print(request.POST)
            product = form.save()
            if product.specialties.all():
                product.previous_specialty_string = product.buildSpecialtiesString()
            print('afte form save',product.specialties.all())
            specialties = form.cleaned_data.get('specialties','')
            product.specialties.clear()
            product.specialties.add(*specialties)
            if product:
                stateCheck = product.checkState(data_s=form.changed_data,object_dict=product_dict)
            if stateCheck:
                print('state check',stateCheck,)
                uht = UserHistoryTable.objects.create(action="2",entity_type="Product",entity_id=product.id,entity_name=product.name,page_link=f"/views/product/detail/{product.id}/",action_verbose=" Product ",action_obj=stateCheck)
                uht.user = request.user
                uht.save()

            messages.success(request,message=f"You have succesfully edited the specialty {product.name}",extra_tags='success')
            return HttpResponseRedirect(reverse('views:viewProductList'))
        print(form.errors)
        return render(request,template_name='support/add_new_product.html',context={'form':form,'product':product})

   
    form = AddProducts(instance=product,initial={'specialties':[specialty.id for specialty in product.specialties.all()]})
    pictureURL = product.picture.url if product.picture else '/media/products/Toes brace/knee_sleeve.png'
    return render(request,template_name='support/add_new_product.html',context={'form':form,'edit':edit,'pictureURL':pictureURL,'product':product})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def editSpecialty(request,id):
    button = 'Update'
    try:
       specialty =  ProductTags.objects.get(id=id)
    except (ProductTags.DoesNotExist,Exception) as error:
        print(error)

    if request.method == 'POST':
        form = AddProductTags(request.POST,request.FILES,instance=specialty)
        if form.is_valid():
            specialty = form.save()
            messages.success(request,message=f"You have succesfully edited the specialty {specialty.tag}",extra_tags='success')
            return HttpResponseRedirect(reverse('views:view_specialties'))
        
        return render(request,template_name='support/add_specialty.html',context={'form':form,'button':button})

    form = AddProductTags(instance=specialty,initial={'products':[product.id for product in specialty.products.all()]})

    return render(request,template_name='support/add_specialty.html',context={'form':form,'button':button})


#  Remove Entities from databse

@login_required
@user_passes_test(lambda u: u.is_superuser )
def removeQsHospital(request,id):
    try:
        qs_hospital = quickStartHospital1.objects.get(id=id)
        qs_hospital.soft_delete = True
        qs_hospital.save()
    except (quickStartHospital1.DoesNotExist,IntegrityError,Exception) as error:
        print(error)
        messages.error(request,f"Error removing hospital {qs_hospital.hospital_name}",extra_tags='warning')
        
    else:
        messages.success(request, f"Succesfully removed hospital  ",extra_tags='success')
       
    return HttpResponseRedirect(reverse('views:view_qs_hospitals'))


def printMe(full_name='fuckyou'):
    print(full_name)
   
def logDeletion(entity,typeE='',flag=False,typeDel='',full_name=''):
    deleteRecord = ''
    try:
        print('logdeltion1')
        restore = '0'
        if flag:
            restore = '3'
        if typeE == 'physician':
            full_name = full_name if full_name else ''
            items = ['specialty_ph','productitems','picture']
            specialty = entity.get('specialty_ph','')
            if specialty:
                entity['specialty_ph'] = list(map(lambda x: x.tag, entity['specialty_ph']))
            else:
                entity['specialty_ph'] = "No Specialties Selected"
            products = entity.get('productitems','')
            if products:
                entity['productitems'] = list(map(lambda x: x.name, entity['productitems']))
            else:
                entity['productitems'] = 'No Products Selected'
            picture = entity.get('picture','')
            if picture:
                entity['picture'] = entity['picture'].url
            else:
                entity['picture'] = "No Picture Provided"
            entity.pop('created_at')

        elif typeE == 'hospital':
            entity.pop['picture']
            entity.pop['created_at']
            entity.pop['picture']
            full_name = entity.get('name','')

        elif typeE == 'product':
            print('stupid bitch')
            full_name = entity.get('name','')


        
        deleteRecord = UserHistoryTable(action=restore,entity_type=typeE,entity_name=full_name,entity_id=entity.get('id',''),action_verbose=f"({typeDel}) Record for ",action_obj=entity)
        deleteRecord.save(dele=True)
        return deleteRecord
    except Exception as error:
        print(error)






@login_required
@user_passes_test(lambda u: u.is_superuser)
def removePhysician1(request,id):
    print("is it coming here")
    selectionDelete = True
    flag = False
    typeDel = ''
    restore = request.GET.get('restore','')
    perm_delete = request.GET.get('perm_delete','')
    sd = True
    uht = ''
    isqs = ''
    try:
        physician = Physician.objects.get(id=id)
        physician_dict = model_to_dict(physician)
        full_name = physician.get_full_name()
       
        print('phdict',physician_dict)
        
    except (Physician.DoesNotExist,IntegrityError,Exception) as error:
        print(error)
    else:
        physician_dict = model_to_dict(physician)
        if restore:
            flag = True
            physician.sd = False
            physician.save()
            print('physician.sd',physician.sd)
            messages.success(request, f"Succesfully Restored Physician {physician.get_full_name()}.",extra_tags='success')

        elif perm_delete:
            if physician.sd:
                typeDel = 'hard'
                physician.delete()
                messages.success(request, f"Permanently removed physician {full_name}. This record will no longer be accessible in deleted physicians.",extra_tags='success')
        else:
            print('came here')
            typeDel = 'soft'
            sd= False
            selectionDelete = ''
            physician.sd = True
            physician.save()
            messages.success(request, f"Succesfully removed physician {physician.get_full_name()}.",extra_tags='success')

        uht = logDeletion(physician_dict,'physician',flag=flag,typeDel=typeDel,full_name=full_name)
        try:
            print('rrrrrr',request.user)
            uht.user = request.user
            uht.save()
        except Exception as fuckubitch:
            print(fuckubitch)
  
    
    physician_set = Physician.objects.filter(sd=sd)
    hospital_set = Hospitals.objects.all()
    #     physician_set = Physician.objects.filter(sd=True)
    # else:
    #     hospital_set = Hospitals.objects.all()t
    #     physician_set = Physician.objects.filter(sd=True)
    revers = f"{reverse('views:view_physicians')}?selectionDelete={selectionDelete}&isqs={isqs}"
    return HttpResponseRedirect(redirect_to=revers)
    return HttpResponseRedirect(reverse('views:view_physicians_staff'))


@login_required
@user_passes_test(lambda u: u.is_superuser)
def removeHospital(request,id):
    try:
        hospital = Hospitals.objects.get(id=id)
        hospital.soft_delete = True
        hospital.save()
    except (Hospitals.DoesNotExist,IntegrityError,Exception) as error:
        print(error)
    else:
        messages.success(request, f"Succesfully removed Hospital  ",extra_tags='success')
        return HttpResponseRedirect(reverse('views:view_hospitals'))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def removeProduct(request,id):
    
    try:
        product = Product.objects.filter(id=id)
        print(product,'product1')
        product_dict = product.values('name','id','short_description','price','previous_specialty_string')[0]
        print(product,'product2')
        product = product[0]
        print(product,'product3')
        product.soft_delete = True
        print(product,'product4')
        product.save()
        print(product,'product4')
        print(product_dict,'producttttt')
        print(product,'product5')
        print(product,'product')
        try:
            # uht = UserHistoryTable(entity_type='product',entity_id=pro)
            uht = logDeletion(product_dict,typeE="product",flag=False,typeDel='soft')
        except Exception as error:
            print(error)
            
        print(product,'product6')
        uht.user = request.user
        print(product,'product7')
        uht.save()
        print(product,'product8')
    except (Product.DoesNotExist,IntegrityError,Exception) as error:
        print(error)
        messages.error(request, f"Error Processing request for deleting product {product.name} ",extra_tags='warning')

    else:
        messages.success(request, f"Succesfully removed Product  ",extra_tags='success')
    return HttpResponseRedirect(reverse('views:view_products'))
    

@login_required
@user_passes_test(lambda u: u.is_superuser)
def removeSpecialty(request,id):
    try:
        specialty = ProductTags.objects.get(id=id)
        specialty.soft_delete = True
        specialty.save()
    except (ProductTags.DoesNotExist,IntegrityError,Exception) as error:
        print(error)
    else:
        messages.success(request, f"Succesfully removed Specialty  ",extra_tags='success')
        return HttpResponseRedirect(reverse('views:view_specialties'))
    
def removePhysicianQs(request,id):
    try:
        qs_physician = quickStartPhysician.objects.filter(id=id)
        qs_physician_dict = qs_physician.values('id','first_name','last_name','products')
        qs_physician = qs_physician[0]
        full_name = qs_physician.get_full_name()
        hospital_name = qs_physician.getHospitalName()
        qs_physician_dict['hospital'] = hospital_name

    except (quickStartPhysician.DoesNotExist,Exception) as error:
        return HttpResponse(f"{error}")
    uht = UserHistoryTable(action='0',entity_type='invited physician',entity_name=full_name,entity_id=qs_physician_dict[0].get('id',''),action_obj=qs_physician_dict)
    uht.user = request.user
    uht.save()
    qs_physician.delete()

    messages.success(request=request,message=f"Uninvited Physician {full_name} from Hospital {hospital_name}",extra_tags='success')
    return HttpResponseRedirect(f"{reverse('views:view_physicians_qs')}?qs=True")
    