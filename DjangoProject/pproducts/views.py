from django.shortcuts import render
from .models import Specialty, ProductTags, Product,Physician
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.core import serializers
import json
from io import BytesIO as IO
import pandas as pd
from django.forms.models import model_to_dict
from django.contrib import messages
from django.urls import reverse
from medical.models import Hospital2
from .helper_functions import sortDict, models2json, returnExcelResponse, rebuildProductList, compareModels
from pproducts.forms import AddProduct2Physician, AddProducts, AddProductTags,AddTags2PhysicianForm, AddHospitalAdmin, LinkedProductTags
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from mysite.settings import ADMIN_CONTACT
from django.contrib.auth.models import User
from woocommerce import API


def is_ajax(request):
  return request.headers.get('x-requested-with') == 'XMLHttpRequest'
"""
physician.html builds a link to displayproducts that shows all products. The only other way to get to products is on the nav bar which is set to display all products
i think there are 3 different values of query parameter view

"""

def products(request):
    """
    keeping the same function when the link is either clicked from the nav bar or clicked from within the physicians table. I will render different HTML. 
    I prob could use one template.

    """
    specialties = ProductTags.objects.all()
    return render(request=request, template_name='pproducts/products.html',context={'specialties': specialties})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def buildHospital(request):

    if request.method == 'POST':
        
        facility_id = request.POST.get('facility', '')
        specialty_name = request.POST.get('specialty', '')
        physician_id = request.POST.get('physician', '')
        specialties = ''
      


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

        else:
            try:
                physicians = list(Physician.objects.all()[0:30].values_list('id','firstName','lastName'))
                specialties = list(ProductTags.objects.all().values_list('id','tag'))
            except Exception as error:
                print(error)
    
        return JsonResponse(data={'dataset': physicians,'specialties':specialties})
            
def buildSpecialties(request):
    if request.method == 'POST':
        
        physician_id = request.POST.get('physicians', '')
      
        specialties = ''
    
        if physician_id and physician_id != 'all':
            try:
                physician = Physician.objects.get(id=physician_id)
            except (Physician.DoesNotExist,Exception) as error:
                print(error)
                specialties = []
            else:
                
                specialties = list(physician.specialty_ph.values_list('id','tag'))
        if not request.user.is_superuser:
            if physician_id and physician_id == 'all':
                try:
                    physicians = request.user.hospital2.physician_set.all()
                except (Exception) as error:
                    print(error)
                tags = list(set([(tag.id,tag.tag) for phy in physicians for tag in phy.specialty_ph.all()]))
        return JsonResponse(data={'dataset':specialties})
    return JsonResponse(data={'dataset': 0})

def filterProducts(request):
    facilities = Hospital2.objects.all() if request.user.is_superuser else ""
    
    productTagProducts = ""
    if request.method == 'POST':
        displayAllOrCurrent = 1
        specialty_model = ''
        specialties = ''
        firstName = ''
        lastName = ''
        specialty_name = request.POST.get('specialty','')
        physician_id = request.POST.get('physician','')
        facility_id = request.POST.get('facility','')
        all_products_hospital = ''
        physician_present = 0
        productitems = ''
        

        if (specialty_name == 'all' and not physician_id):
            displayAllOrCurrent = 0
            products = Product.objects.all()
            productitems = [prod for prod in products]
            productTagProducts = [( model_to_dict(prod), prod.picture.url, 
                                    specialty_name )  if prod.picture else (model_to_dict(prod), 
                                    '/media/uploads/abc.jpeg', specialty_name ) for prod in productitems] if productitems else '' 

            for product in productTagProducts:
                product[0].pop('picture')
        
            superuserFlag = True if request.user.is_superuser else False
            return JsonResponse(data={'dataset': productTagProducts,'physician_id': physician_id,'physician_first':firstName,'physician_last':lastName,'superuser':superuserFlag,'specialties':specialties,'specialty':specialty_name,'tag':specialty_name, 'specialtyid':specialty_model.id if specialty_model else '','physician':physician_present,'allproducts':all_products_hospital,'allorcurrent':displayAllOrCurrent})


        if (specialty_name == 'all' and physician_id == 'all'):
            physician_present = 1
            if facility_id:
                if request.user.is_superuser:
                    physicians_set = Hospital2.objects.filter(id=facility_id)[0].physician_set.all()
            elif not request.user.is_superuser:
                physicians_set = Hospital2.objects.filter(id=request.user.hospital2.id)[0].physician_set.all()
            try:
                productitems= [prod for phy in physicians_set for prod in phy.productitems.all()]
                productitems = list(set(productitems))

            except (IndexError,Exception) as error:
                print("jhhhh")
                print(error)
        
        elif (physician_id == 'all' and specialty_name and specialty_name != 'all'):
            physician_present = 1
            if facility_id:
                try:
                    physicians_set = Hospital2.objects.filter(id=facility_id)[0].physician_set.all()
                    products = LinkedProductTags.objects.filter(physician__in=physicians_set,tag=specialty_name)
                    productitems = list(set([pr for prod in products for pr in prod.products.all()]))
                except (IndexError,Exception) as error:
                    print(error)          
        elif (physician_id and physician_id != 'all' and specialty_name == 'all'):
            physician_present = 1
            try:
                physician = Physician.objects.filter(id=physician_id)[0]
                productitems = physician.productitems.all()
            except (IndexError,Exception) as error:
                print(error)
        elif physician_id and specialty_name:
            physician_present = 1
            try:
            
                physician_model = Physician.objects.get(id=int(physician_id))
                firstName = physician_model.firstName
                lastName = physician_model.lastName
                specialty_model = ProductTags.objects.get(tag=specialty_name)
                productitems = physician_model.linkedtags.filter(tag=specialty_name)[0].products.all()
                physician_present = True
                 
            except (Physician.DoesNotExist, ProductTags.DoesNotExist) as DNE:
                print(DNE)
            except Exception as ERR:
                print(ERR)
        
        elif specialty_name:
            displayAllOrCurrent = 0
            try:
                specialty_model = ProductTags.objects.filter(tag=specialty_name)[0]
                productitems = specialty_model.products.all()    
            except (IndexError, Exception) as error:
                print(error)

        
        productTagProducts = [( model_to_dict(prod), prod.picture.url, 
                                    specialty_name )  if prod.picture else (model_to_dict(prod), 
                                    '/media/uploads/abc.jpeg', specialty_name ) for prod in productitems] if productitems else '' 

        for product in productTagProducts:
            product[0].pop('picture')
        
        superuserFlag = True if request.user.is_superuser else False
        return JsonResponse(data={'dataset': productTagProducts,'physician_id': physician_id,'physician_first':firstName,"allorcurrent":displayAllOrCurrent,'physician_last':lastName,'superuser':superuserFlag,'specialties':specialties,'specialty':specialty_name,'tag':specialty_name, 'specialtyid':specialty_model.id if specialty_model else '','physician':physician_present,'allproducts':all_products_hospital})


def filterAllorCurrent(request):
    if request.method == 'POST':
        valuesForFilter = request.POST.get('filter','')
        productitems = ''
        specialty_id = ''
        if filter:
            valuesForFilter = valuesForFilter.split('-')
            try:
                physician_model = Physician.objects.filter(id=valuesForFilter[2])[0]
            except (IndexError,Exception) as error:
                print(error)
                firstName = ''
                lastName = ''
                physician_model = ''
                specialty_id = ''

            else:
                firstName = physician_model.firstName
                lastName = physician_model.lastName

                if valuesForFilter[0] == 'all':
                    try:
                        productitems = ProductTags.objects.filter(tag=valuesForFilter[1])[0].products.all()
                    except (IndexError,Exception) as error:
                        print(error)   
                else:
                    try:
                        productitems = LinkedProductTags.objects.filter(physician=physician_model,tag=valuesForFilter[1])[0].products.all()
                    except (IndexError,Exception) as error:
                        print(error)

                productTagProducts = [( model_to_dict(prod), prod.picture.url, 
                                        valuesForFilter[1] )  if prod.picture else (model_to_dict(prod), 
                                        '/media/uploads/abc.jpeg', valuesForFilter[1] ) for prod in productitems] if productitems else ''
        try:                         
            specialty_id = ProductTags.objects.filter(tag=valuesForFilter[1])[0].id
        except (IndexError,Exception) as error:
            print(error)

        for product in productTagProducts:
            product[0].pop('picture')
        superuserFlag = True if request.user.is_superuser else False

        return JsonResponse(data={'dataset':productTagProducts,'physician_id':valuesForFilter[2],'physician_first':firstName,'physician_last':lastName,'superuser':superuserFlag,'tag':valuesForFilter[1],'specialty':valuesForFilter[1],'specialty_id':specialty_id,'physician':True})

@login_required
def products_redesign(request):
    hospitals = ''
    if request.user.is_superuser:
        physicians = Physician.objects.all()
        hospitals = Hospital2.objects.all()
    else:
        physicians = Physician.objects.filter(facility=request.user.hospital2)
    specialties = ProductTags.objects.all()
    if request.user.is_superuser:
        return render(request, template_name='pproducts/product_redesign_2.html',context={'physicians':physicians,'specialties':specialties,'facilities':hospitals})
    else:
        return render(request, template_name='pproducts/products_redesign_reg.html',context={'physicians':physicians,'specialties':specialties,'facilities':hospitals})


def  displayProducts(request):

    #TESTING WHAT HAPPENS
    if request.method == "POST":
        
     
        specialty = request.POST.get('specialty')
        physician = request.POST.get('physician_id',False)
     
    
        superuserFlag = True if request.user.is_superuser else False

        if specialty == 'all':
            specialty_id = ''
            specific = request.GET.get('specific','')
            products = Product.objects.all()
            productTagProducts = [( model_to_dict(prod), prod.picture.url )  if prod.picture else (model_to_dict(prod), '/media/uploads/abc.jpeg' ) for prod in products]
            for product in productTagProducts:
                product[0].pop('picture')
            return JsonResponse(data={'dataset': productTagProducts,'superuser':superuserFlag,'specialty':specialty,'tag':specialty, 'specialtyid':''})

        elif int(physician):
            try:
                physician_model = Physician.objects.get(id=int(physician))
            except Physician.DoesNotExist as DNE:
                print(DNE)
                return HttpResponse(f"ERROR MSG {DNE}")
            else:
              
                try:
                    specialty_obj = physician_model.linkedtags.filter(tag=specialty)
                    if specialty_obj:
                        specialty_obj = specialty_obj[0] if specialty_obj else False
                except IndexError as IE:
                    print(IE)
                except Exception as Err:
                    print(Err)
                if not specialty_obj:
                
                    return JsonResponse(data={'dataset':{'clear':'0'}})
                specialty_id = specialty_obj.id

        elif ProductTags.objects.filter(tag=specialty):
              
            specialty_obj = ProductTags.objects.filter(tag=specialty)[0]
            specialty_id = specialty_obj.id
        productTagProducts = [( model_to_dict(prod), prod.picture.url )  if prod.picture else (model_to_dict(prod), '/media/uploads/abc.jpeg' ) for prod in specialty_obj.products.all()]
     
        for product in productTagProducts:
            product[0].pop('picture')
    
        superuserFlag = True if request.user.is_superuser else False
  
        
        return JsonResponse(data={'dataset': productTagProducts,'superuser':superuserFlag,'specialty':specialty,'tag':specialty, 'specialtyid':specialty_id})

    specialty = request.GET.get('specialty',False)
    specialty = specialty.lower() if specialty else False
    view = request.GET.get('view',"").lower()
    physician = int(request.GET.get('physician',0))
  
    allTags = ProductTags.objects.all().order_by('tag')
    
    try:
        physician_model = Physician.objects.filter(id=physician)[0]
        products = physician_model.linkedtags.get(tag=specialty).products.all()
    except (Physician.DoesNotExist,LinkedProductTags.DoesNotExist,IndexError) as DNE:
        print(DNE)
        products = ProductTags.objects.filter(tag=specialty)[0].products.all()
        first_name = ""
        last_name = ""
    else:
        allTags = physician_model.specialty_ph.all()
        first_name = physician_model.firstName
        last_name = physician_model.lastName
    
    id = physician_model.id if physician_model else 0
    return render(request=request, template_name='pproducts/products.html',context={'physician_name_first':first_name,'physician_name_last':last_name,'physician_id': id,'specialtyTags':products,'view':view,'tag':specialty,'specialties':allTags})

@login_required
def physician(request):
    data_label = "physician"
    hospitals = ""
    view = 'all'
    
    hospitals = Hospital2.objects.all().order_by('name')
    if request.user.is_superuser:
        if request.method == 'POST':
            hospital_id = request.POST.get('select-hospital',0)
            # performing filter lookup upon dropdown
            if id:
                if hospital_id == 'all':
                    physicians = Physician.objects.all()
                else:
                    hospital_id = int(hospital_id)
                    hospital = Hospital2.objects.filter(id=hospital_id)[0]
                    physicians = hospital.physician_set.all() 
                    view = False
            return render(request=request, template_name='pproducts/physician.html',context={'physicians': physicians,'view':view, 'data_label':data_label,'hospitals': hospitals,'hospital_id':hospital_id})
        else:  
            physicians = Physician.objects.all()
    else:
        physicians = Physician.objects.filter(facility=request.user.hospital2)


    
    return render(request=request, template_name='pproducts/physician.html',context={'physicians': physicians, 'data_label':data_label,'hospitals': hospitals})
   
@login_required    
def addphysician(request):
  
    from .forms import AddPhysician, AddPhysicianAdmin
    editornew = request.GET.get('edit', False)
   
    header = 'Add Physician'
    button_text = 'Add Physician'
    
    if request.method == 'POST':
     
        facility = request.POST.get('facility', False)
      
        if request.user.is_superuser:
            try:
                
                print(type(facility))
                hospital = Hospital2.objects.get(id=facility)
                form = AddPhysicianAdmin(request.POST, request.FILES)
            except (Hospital2.DoesNotExist,ValueError) as hdne:
                print(hdne)
                messages.error(request, "Error Assigning to Hospital. Please Contact Administrator ")
                return HttpResponseRedirect(reverse('pproducts:addphysician'))
            else:
                print("does it make iteweqewqew")
                if form.is_valid():
                    print('does it make it here2')
                    pushtowoo = request.POST.get('pushtowoo','')
                    #test if specialty_ph is none which means they filled out nothing
                    post = dict(request.POST)
                    post.update(form.cleaned_data)
                    post.pop('csrfmiddlewaretoken')
                    print(post)
                    physician = form.save(post,hospital=hospital ,commit=True, admin=request.user,action='Created')
                    if pushtowoo == 'create' or pushtowoo == 'update':
                        physician.sendToWooCommerce(updateOrCreate=pushtowoo)

                    messages.success(request, f"Successfully added a physician {physician.firstName} {physician.lastName}")
                    return HttpResponseRedirect(reverse('medical:dashboard'))
                else:
                    print()
                    messages.warning(request,"Please Review Errors and Resubmit form.")
                    return render(request, template_name='pproducts/addphysician.html',context={'form':form,'button_text': button_text, 'header': header})

        else:
            form = AddPhysician(request.POST, request.FILES)
            if form.is_valid():
                post = dict(request.POST)
                post.update(form.cleaned_data)
                post.pop('csrfmiddlewaretoken')
                physician = form.save(post,hospital = request.user.hospital2,commit=True,admin = request.user, action='Created')
                msg = f"Successfully added a physician {physician.firstName} {physician.lastName}"
                messages.success(request=request,message= "Successfully added a physician.")
                return HttpResponseRedirect(reverse("medical:dashboard"))
        
            else:
                messages.warning(request,"Please Review Errors and Resubmit form.")
                return render(request, template_name='pproducts/addphysician.html',context={'form':form,'button_text': button_text, 'header': header})

    if request.user.is_superuser:
        form = AddPhysicianAdmin()
    else:
        form =AddPhysician(initial={'facility':request.user.hospital2})

    return render(request, template_name='pproducts/addphysician.html', context={'form':form, 'button_text': button_text, 'header': header})

@login_required
def edit_physician(request,id):
    from .forms import AddPhysician,AddPhysicianAdmin
    physician = Physician.objects.filter(id=id)[0]

    if request.method == 'POST':
      
        if request.user.is_superuser:
            facility = request.POST.get('facility', "")
            try:
                hospital = Hospital2.objects.get(id=facility)
                
                form = AddPhysicianAdmin(request.POST, request.FILES, instance=physician)
            except Hospital2.DoesNotExist as hdne:
                print(hdne)
                messages.error(request, "Error Assigning to Hospital. Please Contact Administrator ")
                return HttpResponseRedirect(reverse('medical:contactus'))
            else:
                if form.is_valid():
                    
                    post = dict(request.POST)
                    post.update(form.cleaned_data)
                    post.pop('csrfmiddlewaretoken')
                    updated_physician = form.save(post,hospital =hospital, commit=True,action='Updated', admin=request.user)

                    msg = f"Successfully updated physician w/ First: {updated_physician.firstName} Last: {updated_physician.lastName} @ {hospital.name}"
                    messages.success(request,message=msg)
                    return HttpResponseRedirect(reverse('pproducts:physician'))
        else:
            print("edit physician does it come here bro")
            form = AddPhysician(request.POST,request.FILES,instance=physician)
            if form.is_valid():
                post = dict(request.POST)
                post.update(form.cleaned_data)
                post.pop('csrfmiddlewaretoken')
                updated_physician = form.save(post,hospital =request.user.hospital2, commit=True,admin=request.user,action='Updated')
                # if form.changed_data:
                #     print("changed motherfucker")
                #     updated_physician.save()
                #     history = updated_physician.history.latest()
                #     history.history_change_reason = f"{request.user.username} Updated Physician {updated_physician.firstName} {updated_physician.lastName}."
                #     history.save()
                #     physician.save_no_history()

                msg = f"Successfully updated physician: First: {updated_physician.firstName} Last: {updated_physician.lastName} @ {request.user.hospital2.name}"
                messages.success(request,message=msg)
                return HttpResponseRedirect(reverse('pproducts:physician'))

        tag = request.GET.get('specialty',False)
        specialty = ProductTags.objects.filter(tag=tag)
        # specialty = ProductTags.objects.filter(physicians=physician) 
        messages.error(request, "Please correct errors below and re-submit.")
        return render(request, template_name='pproducts/edit_physician.html',context={'header': 'Edit Physician', 'button_text':'Update Physician' ,'form': form,'physician':physician,'specialty': specialty})
    
    if physician.productitems:
        allProducts, physician_specialties = rebuildProductList(physician=physician)
    else:
        pass
    edit = False

    if request.user.is_superuser:
        form = AddPhysicianAdmin(instance=physician,initial={'specialty_ph':physician_specialties})
    else:
        form = AddPhysician(instance=physician,initial={'specialty_ph':physician_specialties})
    
    return render(request, template_name='pproducts/edit_physician.html',context={'header': 'Edit Physician', 'button_text':'Update Physician' ,'editproductslist':allProducts,'form': form,'edit':edit})

def  displayPhysicians(request):
    id = request.POST.get('hospital',999)
    physicians = Hospital2.objects.filter(id=id)[0].physician_set.all()
    

    return render

def productsFilter(request):
    view = request.GET.get('view',False)

    if view == 'current':
        pass

@login_required
@user_passes_test(lambda u: u.is_superuser)
def addProduct(request):
    header = "Add New Product"
    button = "Add Product"
    new = True
    if request.method == 'POST':
        form = AddProducts(request.POST,request.FILES)
        if form.is_valid():
            specialty_list = request.POST.getlist('specialties')
            product = form.save(specialties=specialty_list)
            product.logHistory(user=request.user.username,created=True)
            pushtoowoo =form.cleaned_data.get("pushtowoo","")
            if pushtoowoo == 'update' or pushtoowoo == 'create':
                product.sendToWooCommerce(updateOrCreate=pushtoowoo)

            messages.success(request,f"Succesfully Added New Product {product.name} w/ Specialties {list(product.specialties.all())}")
            return HttpResponseRedirect(reverse('pproducts:products'))

        messages.warning(request, "Please See the Form Below for Errors ")
        return render(request,template_name='pproducts/edit_product.html',context={'form':form,'header':header, 'button':button})

    form = AddProducts()
    print("rigt")
    return render(request,template_name='pproducts/edit_product.html',context={'form':form,'header':header, 'button':button})
# THIS MAY CAUSE PROBLEMS!!!!!!!
def removeProduct(request,id):

    try:
        product_model = Product.objects.get(id=id)
        product_name = product_model.name
        specialties = [specialty.tag for specialty in product_model.specialties.all() ]
        label = f"Are you sure you want to remove {product_model.name}? If removed the product will be removed from the following specialties {specialties}" 

    except (ProductTags.DoesNotExist, Exception) as Error:
        print(Error)
        return HttpResponseRedirect(reverse('medical:dashboard'))
    if request.method == 'POST':
        approval = request.POST.get('app_butt','')
        if approval:
            product_model.delete()
            messages.success(request=request, message=f"You have succesfully deleted the product {product_name} from the following specialties {specialties}")
            return HttpResponseRedirect(reverse('medical:dashboard'))
        return HttpResponseRedirect(reverse('medical:dashboard'))
    view = 'deletespecialty'
    return render(request, template_name='medical/approvalconfirm.html', context={'view': view,'product_id':id,'tag':product_model,'specialties':specialties})


def pullFromWooCommerce(request):
    if request.method == 'POST':
        json = ''
        label = ''
        wcapi = API(
                url=WOOCOMMERCE_API_URL_DEV,
                consumer_key=WOOCOMMERCE_CUSTOMER_KEY,
                consumer_secret=WOOCOMMERCE_CUSTOMER_SECRET,
                version="wc/v3",
                timeout = 10
            )
        fromwoo = request.POST.get('from-woo-pull-type','')
        try:
            if fromwoo == 'products':
                json = wcapi.get("products").json()
                label = "Product"
            #Categories is Physicians in woocommerce
            elif fromwoo == 'categories':
                json = wcapi.get("products/categories").json()
                label = "Physician"
            elif fromwoo == "tags":
                json = wcapi.get("products/tags").json()
                label = "Tag"
        except (Exception,TimeoutError) as error:
            print(error)
            messages.error(request,message="There was an error pulling data from WooCommerce. Please try again later.")
        return render(request,template_name='pproducts/fromwoo.html',context={"woodata":json,"flag":True,"label":label})
    return render(request,template_name='pproducts/fromwoo.html',context={})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def editproduct(request,id):
    header = "Edit Product"
    button = "Update"
    if request.user.is_superuser:
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist as PDNE:
            print(PDNE)
            messages.error(request, message="Please Correct Errors and Re Submit")
            return HttpResponseRedirect(reverse('pproducts:editproduct', args=(id,)))
        else:
            if request.method == 'POST':
                image = request.FILES.get('image','')
                pushtowoo =request.POST.get('pushtowoo')
                print(request.FILES)
                form = AddProducts(request.POST, request.FILES, instance=product)
                if form.is_valid():
                    product = form.save(commit=True)
                    print('pushtowii',pushtowoo)
                    if pushtowoo == 'create' or pushtowoo == 'update':
                        product.sendToWooCommerce(updateOrCreate = pushtowoo)
                    if form.changed_data:
                        product.logHistory(user=request.user.username)
                        messages.success(request, f"Succesfully Updated Product {product.name}")
                    
                    return HttpResponseRedirect(reverse('pproducts:products'))
                messages.error(request,message="Please Review Errors and re Submit")
                return render(request,template_name='pproducts/edit_product.html',context={'form':form,'header':header, 'button':button,'product_id':id,'new':True})
            form = AddProducts(instance=product,initial={'specialties':[product.id for product in product.specialties.all()]})
            return render(request,template_name='pproducts/edit_product.html',context={'form':form,'header':header, 'button':button,'product_id':id,'new':True})
    else:
        messages.error(request, message="Only SuperUsers can Edit or Add Products. Please contact administrator for details.")
        return HttpResponseRedirect(reverse('medical:dashboard'))

def addTags(request):
    header = "New Specialty"
    button = "Add Specialty"
    if request.method == 'POST':
        form = AddProductTags(request.POST)
        if form.is_valid():
            productTag = form.save(commit=True)
            productTag.logHistory(user=request.user.username,created=True)

            messages.success(request, message=f"Specialty has been succesfully added. You can now assign Physicians to the Specialty {productTag.tag}.")
            return HttpResponseRedirect(reverse('medical:dashboard'))
    else: 
        form = AddProductTags()
    return render(request, template_name='medical/contactus1.html', context={'form':form,'header':header,'button':button})

def editTags(request,id):
    header = "Edit Specialty"
    button = "Update Specialty"
    try:
        tag = ProductTags.objects.get(id=id)
        
    except ProductTags.DoesNotExist as PTDNE:
        print(PTDNE)
        messages.error(request, "Tag Can Not Be Updated. Please contact the administrator at {ADMIN_CONTACT} ")
    else:
        if request.method == 'POST':
            child_tags = tag.parenttags.all()
            form = AddProductTags(request.POST, instance=tag)
            if form.is_valid():
                tag = form.save(child_tags=child_tags,commit=True)
                if form.changed_data:
                    tag.logHistory(user=request.user.username)
                    messages.success(request,message=f"Succesfully Updated {tag.tag}")

                return HttpResponseRedirect(reverse('pproducts:products'))
        else:
            form = AddProductTags(initial={'specialties':[product.id for product in tag.products.all()]},instance=tag)
    return render(request, template_name='medical/contactus1.html', context={'form':form,'header':header,'button':button})

@login_required
def product2physician(request,id):
    from django.forms.models import model_to_dict
    try:
        product = Product.objects.filter(id=id)[0]
    except (IndexError,Exception) as err:
        print(err)
        messages.error(request,"The Product could not be updated. If the problem persists, please contact the administrator at wajahathassan@blahblah.com. ")
        return HttpResponseRedirect('medical:dashboard')
    if request.method == 'POST':
        product_id = request.POST.get("product")

        product = Product.objects.filter(id=product_id)[0]
        
        product_dict = model_to_dict(product)
   
        physicians = request.POST.getlist('physician')
      
        physicians_set = Physician.objects.filter(id__in=physicians)

        specialty = request.POST.get('specialty', False)
        specialty = specialty.lower() if specialty else ""
        if isinstance(specialty,str) and specialty:
            specialty = specialty.lower()
        
        if not isinstance(product_dict.get('picture',False), str):
            product_dict['picture'] = product_dict['picture'].url if product_dict.get('picture',False) else "N/A"
    
        # info_text = f"Updated Products. Added {product.name} for "
        for physician in physicians_set:
            # info_text +=  physician.firstName + physician.lastName + " "
            physician.updateProductsList(specialty=specialty,product=product)
        # info_text += f"@ hospital {request.user.hospital2.name}"
        return HttpResponseRedirect(reverse('pproducts:physician'))

    
    specialty = request.GET.get('specialty','')
    specialty_tag = ProductTags.objects.filter(tag=specialty)[0]
    
    if not request.user.is_superuser:
        physicians = Physician.objects.filter(facility=request.user.hospital2)
    else:
        physicians = Physician.objects.all()

    return render(request, template_name='pproducts/addproduct2physician.html', context={'product':product,'specialty':specialty_tag,'physicians': physicians,'id': id})

def testifworks(request,id=None):
    from .forms import AddPhysician, AddPhysicianAdmin
    editornew = request.GET.get('edit', False)
    header = 'Add Physician'
    button_text = 'Add Physician'
    queryset = ProductTags.objects.all().order_by('tag')
    if request.method == 'POST':
        facility = request.POST.get('facility', "")
        if request.user.is_superuser:
            try:
                hospital = Hospital2.objects.get(id=facility)
                form = AddPhysicianAdmin(request.POST, request.FILES)
            except Hospital2.DoesNotExist as hdne:
                print(hdne)
                messages.error(request, "Error Assigning to Hospital. Please Contact Administrator ")
                return HttpResponseRedirect(reverse('medical:contactus'))
        else:
            form = AddPhysician(request.POST, request.FILES)
        if form.is_valid():
            if request.user.is_superuser:
                physician = form.save(request.POST,hospital ,commit=True)
            else:
                physician = form.save(request.POST,request.user.hospital2,commit=True)

            physician.resizeImage()
            msg = f"Successfully added a physician to"
            messages.success(request, "Successfully added a physician.")
            return HttpResponseRedirect(reverse("medical:dashboard"))
        else:
            messages.warning(request,"Please Review Errors and Resubmit form.")
            return render(request, template_name='pproducts/addphysician.html',context={'form':form,'button_text': button_text, 'header': header, 'tags': queryset})
    if request.user.is_superuser:
        form = AddPhysicianAdmin()
    else:
        form =AddPhysician()
    return render(request, template_name='pproducts/addphysician.html', context={'form':form, 'button_text': button_text, 'header': header, 'tags': queryset})

@login_required
def rfsh_products(request):
    if is_ajax(request):

            tags = request.POST.getlist("lookup[]")

            updateProductList =  {tag:list(ProductTags.objects.filter(tag=tag)[0].products.all().values()) for tag in tags}

            return JsonResponse(data={'dataset': updateProductList})

@login_required
def downloadXLS(request):
    datatype = request.GET.get('datatype', 'none') 
    if datatype == 'products':
        physicians = Physician.objects.all()
        dataframe = pd.DataFrame(physicians.values()).set_index('id')
        sheet = 'physicians'
        file_name = 'physicians'
    elif datatype == 'admin':
        admin_staff = User.objects.all().exclude(is_superuser=True).order_by('last_name')
        print(admin_staff)
        dataframe = pd.DataFrame(admin_staff.values()).set_index('id')
        dataframe[['last_login','date_joined']] = dataframe[['last_login','date_joined']].astype(str)
        sheet = 'admins'
        file_name='admins'

    else:
        from medical.models import Hospital2
        hospitals = Hospital2.objects.all().defer('created_at','modified_at')
        dataframe = pd.DataFrame(hospitals.values()).set_index('id')
        dataframe[['modified_at','created_at','approved_at']]=dataframe[['modified_at','created_at','approved_at']].astype(str)
        sheet = 'hospitals'
        file_name = 'hospitals'

    return returnExcelResponse(dataframe=dataframe,sheet=sheet, file_name=file_name)

def addTags2Physician1(request,id):
 
    physician = Physician.objects.filter(id=id)[0]
    editFlag = request.GET.get('edit',False)
    physician_full_name = f"{physician.firstName} {physician.lastName}"
    button_text = "Assign Specialties"
    header = "Update Specialties"
    queryset = ProductTags.objects.all()
    if request.method == 'POST':
        form = AddTags2PhysicianForm(request.POST, instance=physician)
        if form.is_valid():
            post = dict(request.POST)
            post.update(form.cleaned_data)
            post.pop('csrfmiddlewaretoken')
            physician = form.save(obj=post,commit=True,admin=request.user,action='Updated')
            # physician
            # physician.update_history_record(admin =  request.user, action='created')

            print("-------------------END OF ADDTAGS@PHYSCIAN--------------------")
            messages.success(request=request, message=f"Succesfully updated Physician {physician.get_full_name()}")
            return HttpResponseRedirect(reverse('pproducts:physician'))
        messages.warning(request, f"There was an error processing your request. If this problem is reoccuring please contact the Administrator {ADMIN_CONTACT}")
        if editFlag == 'true':
            allProducts, physician_specialties = rebuildProductList(physician=physician)
            return render(request, template_name='pproducts/edit_physician.html', context={'form':form, 'button_text': button_text, 'header': header,'editproductslist':allProducts,'edit':False })

        return render(request, template_name='pproducts/addphysician.html', context={'form':form, 'button_text': button_text, 'header': header, 'tags': queryset})

    form = AddTags2PhysicianForm(instance=physician)

    if editFlag == 'true':
        allProducts, physician_specialties = rebuildProductList(physician=physician)
        return render(request, template_name='pproducts/edit_physician.html', context={'form':form, 'button_text': button_text, 'header': header,'editproductslist':allProducts,'edit':False })

    return render(request, template_name='pproducts/addphysician.html', context={'form':form, 'button_text': button_text, 'header': header, 'tags': queryset})

def assignFacilityAdmin(request,id):
    button_text = 'Assign Facility'
    header = 'Add New Facility'
    physician = Physician.objects.filter(id=id)[0]
    if request.method == 'POST':
        form = AddHospitalAdmin(request.POST,instance=physician)
        if form.is_valid():
            physician = form.save(commit=True)
            messages.success(request, message= f"Succesfully assigned {physician.facility.name} to First: {physician.firstName.title()} Last: {physician.lastName.title()}")
            return HttpResponseRedirect(reverse('pproducts:physician'))
        messages.warning(request, message=f"Hospital could not be assigned to the Physician First: {physician.firstName.title()} {physician.lastName.title()}.")
        return render(request,template_name='medical/contactus1.html', context={'form': form})

    form = AddHospitalAdmin(instance=physician)
    return render(request,template_name='medical/contactus1.html', context={'form': form,'header':header, 'button_text':button_text})

def removephysician(request,id):

    physician = Physician.objects.filter(id=id)[0]

    if request.method == 'POST':
        
        firstName =  physician.firstName
        lastName = physician.lastName
        facility = physician.facility.name
        value = request.POST.get("approval", "")
        # return HttpResponse(f"{physician} {value}")
        # value = request.POST.get("approval", "")
        if value:
            del_physician = physician.delete()
        
            messages.success(request, message=f"You have succesfully deleted First: {firstName} Last: {lastName} @ {facility}")
        
        return HttpResponseRedirect(reverse('pproducts:physician'))

    label = f"Are you sure you want to remove the selected physician First {physician.firstName} Last {physician.lastName} @ Facility {physician.facility.name}"
    return render(request=request,template_name='pproducts/removephysician.html',context={'physician':physician,'label':label})



"""

productTagProducts = [( model_to_dict(prod), prod.picture.url, prod.linkedproducttags_set.filter(physician=jack,products__id=prod.id)[0].parentTag.tag )  if prod.picture else (model_to_dict(prod), '/media/uploads/abc.jpeg',prod.linkedproducttags_set.filter(physician=jack,products__id=prod.id)[0].parentTag.tag ) for prod in productitems]


"""