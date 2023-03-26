
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from pproducts.models import Physician, Specialty, ProductTags, Product, LinkedProductTags
import json
from pproducts.serializers import PhysicianSerializer 
from django.forms.models import model_to_dict
from pproducts.helper_functions import sortDict, debuggingCode
from rest_framework.renderers import JSONRenderer
# from pproducts.models import  JsonProducts
from django.utils import timezone
from django.utils import timezone, dateformat
from django.core.exceptions import ValidationError
from medical.models import Hospital2

def pp(self):
        return f"First: {self.firstName} Last:{self.lastName} \n Specialties \n {self.specialty_ph.all()} \n Products \n {self.productitems.all()} \n Products(JSON) \n {self.products} \n END OF PHYSICIAN"

class AddProduct2Physician(forms.Form):

    physicians = forms.ModelMultipleChoiceField(required=True,label="Physicians",widget=forms.CheckboxSelectMultiple(attrs={'id':'id_select_box2','name':'physician','data-tbl':'physician'}), queryset=Physician.objects.all().order_by('firstName'))
    class Meta:
         exclude=['products','productitems','previous_state','productitems_previous']

class AddPhysicianAdmin(ModelForm):
    CHOICES = (
        ("", "Push To WooCommerce" ),
        ('create', 'New Physician(Category)'),
        ('update', 'Update Physician(Category)'),
        ("no_push", 'Do Not Push'),
    )
    hospital = forms.ModelChoiceField(queryset=Hospital2.objects.all().order_by('name'),widget=forms.Select(attrs={'onchange':'populateName(event)','id':'hospitalModelField'}),required=False)
    pushtowoo = forms.ChoiceField(label="",required=False,widget=forms.Select(attrs={"onchange": "populateDropDown(event)"}),choices=CHOICES)
    shop_recovery_id = forms.IntegerField(required=False,label="Woo Commerce ID", widget=forms.NumberInput(attrs={"id":"shop-recovery-id","class":"whatthefuck","style":"display:none;"}))
    specialty_ph = forms.ModelMultipleChoiceField(required=False,label="Specialty Areas",widget=forms.SelectMultiple(attrs={'onchange':'refreshProducts2(event)','id':'id_select_box2'}), queryset=ProductTags.objects.all().order_by('tag'))
    shop_recovery_name = forms.CharField(widget=forms.TextInput(attrs={"style":"display:none;","id":"shop_recovery_name"}), required=False)
    class Meta:
        model = Physician
        fields = ['pushtowoo','shop_recovery_id','shop_recovery_name','picture','firstName','lastName','email','hospital','about_me']
        # exclude=['products','productitems','previous_state','productitems_previous']
        labels = {
            'firstName': 'First Name',
            'lastName': 'Last Name',
            'shop_recovery_name': 'Woo Commerce Name'
        }

    def __init__(self, *args,new=False, **kwargs):
        super(AddPhysicianAdmin, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if new:
                visible.field.widget.attrs['class'] = 'form-control'
            else:
                if visible.name == "specialty_ph":
                    visible.field.widget.attrs['class'] = 'form-control icon_gap special_id'
                else:
                    visible.field.widget.attrs['class'] = 'form-control icon_gap'
                if visible.name =='picture':
                    visible.field.widget.attrs['id'] = 'formFile'
    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control'

    #         if visible.name == 'picture':
    #             visible.field.widget.attrs['id'] = 'formFile'           
                
    def save2Json(self,physician={},obj={}):
        products={}
        
        physician.productitems.clear()
        for key,value in obj.items():
            if "prod-" in key:
                specialty_key = key.split('-')[1]
                # get the list of selected products from the post request
                selected_product_list = obj.get(key)
                productitems =  Product.objects.filter(id__in=selected_product_list)
                products[specialty_key] = []
                print("selected product list",selected_product_list)
                for record in productitems:
                    if str(record.id) in selected_product_list:
            
                        modelToDict = physician.convertObject(record)
                        print('MODELTODICT',modelToDict)
                        products[specialty_key].append(modelToDict)
                        physician.productitems.add(record)
                        self.createLinkedTag(physician=physician,specialty=specialty_key,product=record)
    
        # if not physician.productitems_previous:
        #     holding = {}
        #     holding['main'] = list(physician.productitems.all().values('id','name'))
        #     physician.productitems_previous = holding
            
        debuggingCode(f"Model2Physician.save()", 58, f"physician.products (After ReBuilding Json) {products}")

        return products
    def compareProducts(self):
        pass

    def createLinkedTag(self,specialty,product,physician):
        # if physician.linkedtags.all()) <= len(physician.)
        try:
            linked_product = LinkedProductTags.objects.get(physician=physician,tag=specialty)
        except LinkedProductTags.DoesNotExist as DNE:
            try:
                parentTag = ProductTags.objects.filter(tag=specialty)[0]
            except IndexError as IE:
                print(IE)
            else:
                linkedTag = LinkedProductTags.objects.create(parentTag=parentTag,physician=physician,tag=specialty)
                linkedTag.products.add(product)
                linkedTag.save()
                physician.linkedtags.add(linkedTag)
                
        except Exception as Error:
            print(Error)
        else:
            if product not in linked_product.products.all():
                linked_product.products.add(product)
                linked_product.save()
                
    def removeDifferencefromDeletedTags(self,physician):
        specialties = physician.specialty_ph.all()
        new_specialties = physician.linkedtags.exclude(parentTag__in=specialties)
        physician.linkedtags.remove(*new_specialties)
        physician.save()

    def save(self,obj={},hospital=None,commit=True,flag=False,approved_by='',admin='',action=''): 

        print('obj',obj)
   
        physician = super().save(commit=False)

        if flag:
            return physician

        if hospital:
            physician.save()
            physician.facility = hospital
            physician.save()
       
        # # print(f"Function: AddTags2Physician.save() Line: 62 pproducts/forms.py Additional Data: \n 1. Physician.Products- {physician} \n 2: Product Items- {physician.productitems.all()}")
        # products = self.save2Json(physician=physician,obj=obj)

        # physician.products = sortDict(products)
            # serial_obj = PhysicianSerializer(physician).data
            # bytes = JSONRenderer().render(data=serial_obj)
            # JsonProducts.objects.create(bytes=bytes,products=serial_obj, physician=physician)
    
        if commit:
            print("obj",obj)
            specialties = obj.get('specialty_ph')
            print(specialties)
            physician.specialty_ph.add(*specialties)
            physician.save()
            self.save_m2m()
            print('physicians',physician.specialty_ph.all())
            # self.removeDifferencefromDeletedTags(physician=physician)
        
        # if self.changed_data:
        #     physician.save()
        #     self.save_m2m()
        #     earliest_record = physician.history.latest()
        #     earliest_record.history_change_reason = f"{admin.username} {action} New Physician {physician.firstName} {physician.lastName} for {facility_name}"
        #     earliest_record.save()
        #     physician.save_no_history()
        
        return physician
    
class AddTags2PhysicianForm(AddPhysicianAdmin):
  
    class Meta:
        model = Physician
        fields = ['specialty_ph']

class AddPhysician(AddPhysicianAdmin):
    # pushtowoo = forms.ChoiceField(label="",required=True,widget=forms.Select(attrs={"onchange": "populateDropDown(event)"}),choices=CHOICES)
    # shop_recovery_id = forms.IntegerField(required=False,label="Shop-Recovery ID", widget=forms.NumberInput(attrs={"id":"shop-recovery-id"}))
    specialty_ph = forms.ModelMultipleChoiceField(required=False,label="Specialty Areas",widget=forms.SelectMultiple(attrs={'onchange':'refreshProducts2(event)','id':'id_select_box2'}), queryset=ProductTags.objects.all().order_by('tag'))

    class Meta:
        model = Physician
        fields = ['picture','about_me','firstName','lastName','email','description','services']

        # exclude=['products','productitems','facility','previous_state','productitems_previous']
        labels = {
            'firstName': 'First Name',
            'lastName': 'Last Name'
        }

    def __init__(self, *args,new=False, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name == 'hospital':
                visible.field.widget.attrs['style'] = 'display:none;'

            if new:
                visible.field.widget.attrs['class'] = 'form-control'
            else:
                if visible.name == "specialty_ph":
                    visible.field.widget.attrs['class'] = 'form-control icon_gap special_id'
                else:
                    visible.field.widget.attrs['class'] = 'form-control icon_gap'
                if visible.name =='picture':
                    visible.field.widget.attrs['id'] = 'formFile'
    
    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control'

    #         if visible.name == 'picture':
    #             visible.field.widget.attrs['id'] = 'formFile'
        
class AddProductTags(ModelForm):


    CHOICES = (
    ("", "Push To WooCommerce" ),
    ('create', 'New Tag(Specialty)'),
    ('update', 'Update Tag(Specialty)'),
    ("no_push", 'Do Not Push'),
)
    
    pushtowoo = forms.ChoiceField(label="",required=False,widget=forms.Select(attrs={"onchange": "populateDropDown(event)"}),choices=CHOICES)

    class Meta:
        model = ProductTags
        exclude = []

    def __init__(self, *args, **kwargs):

        super().__init__(*args,**kwargs)
        for visible in self.visible_fields():
            
            visible.field.widget.attrs['class'] = 'form-control'
            if visible.name == 'shop_recovery_id':
                visible.field.widget.attrs['id'] = 'id_shop_recovery_id'
            elif visible.name == 'tag':
                visible.field.widget.attrs['id'] = 'tag'
            elif visible.name == 'description':
                visible.field.widget.attrs['id'] = 'product_long_description'
            elif visible.name == 'products':
                visible.field.widget.attrs['id'] = 'id_products'
            # if visible.name == 'id_shop_recovery_id'


            # if visible.name == 'picture':
            #     visible.field.widget.attrs['id'] = 'formFile'
            # if visible.name == 'short_description':
            #     visible.field.widget.attrs['id'] = 'product_short_description'
            #     visible.field.widget.attrs['rows'] = '5'
            #     visible.field.widget.attrs['cols'] = '20'
            # if visible.name == 'description':
            #     visible.field.widget.attrs['id'] = 'product_long_description'

class AddHospitalAdmin(ModelForm):
    
    class Meta:
        model = Physician
        fields = ['facility']

class AddProducts(ModelForm):
    CHOICES = (
        ("", "Push To WooCommerce" ),
        ('create', 'New Product'),
        ('update', 'Update Product'),
        ("no_push", 'Do Not Push'),
    )
    #widget=forms.FileInput(attrs={'name':'pictureImage', 'width': '100', 'height': '100'})
    # product_image = forms.ImageField(label="Product Image",required=False)
    shop_recovery_id = forms.IntegerField(required=False,label="Shop-Recovery ID", widget=forms.NumberInput(attrs={"id":"shop-recovery-id"}))
    pushtowoo = forms.ChoiceField(label="",required=False,widget=forms.Select(attrs={"onchange": "populateDropDown(event)"}),choices=CHOICES)
    specialties = forms.ModelMultipleChoiceField(required=False,widget=forms.SelectMultiple(attrs={'name':'specialties'}),queryset=ProductTags.objects.all())
    price = forms.CharField(required=False,widget=forms.TextInput(attrs={}))
    class Meta:
        model = Product
        exclude=['created_at','updated_at']
        fields = ['pushtowoo','shop_recovery_id','name','description','short_description','price','quantity','category','picture','manufacturer','UPC','SKU','specialties']

    def __init__(self, *args,fields=[], **kwargs):

        super().__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

            if visible.name == 'picture':
                visible.field.widget.attrs['id'] = 'formFile'
            if visible.name == 'short_description':
                visible.field.widget.attrs['id'] = 'product_short_description'
                visible.field.widget.attrs['rows'] = '5'
                visible.field.widget.attrs['cols'] = '20'
            if visible.name == 'description':
                visible.field.widget.attrs['id'] = 'product_long_description'


    def clean(self, *args, **kwargs):

        pushtowoo = self.cleaned_data.get('pushtowoo','')
        shop_recovery_id = self.cleaned_data.get('shop_recovery_id','')
        specialties = self.cleaned_data.get('specialties','')

        if pushtowoo == 'create':
            if shop_recovery_id:
                raise ValidationError("Shop recovery ID must be left blank if creating a new product. Woo Commerce Auto Generates ID's")
        elif pushtowoo == "update":
            if not shop_recovery_id:
                raise ValidationError("Please provide an a valid shop-recovery product ID when performing an update.")
        
        cleaned_data = super().clean(*args,**kwargs)
        return cleaned_data

    def save(self,specialties=[],commit=True):
        product = super().save(commit=False)
        if commit:
            product.save()
            
            self.save_m2m()
            # print('specialties',product.specialties.all())
        return product
          
# class AddProductTags(ModelForm):

#     class Meta:
#         model = ProductTags
#         exclude=['related_specialty']
#         required_fields = ['tag']

#     def __init__(self, *args, **kwargs):

#         super().__init__(*args,**kwargs)
#         for visible in self.visible_fields():
#             print(visible.name)
#             visible.field.widget.attrs['class'] = 'form-control'
#             if visible.name == 'shop_recovery_id':
#                 visible.field.widget.attrs['id'] = 'id_shop_recovery_id'
#             elif visible.name == 'tag':
#                 visible.field.widget.attrs['id'] = 'tag'
#             elif visible.name == 'description':
#                 visible.field.widget.attrs['id'] = 'product_long_description'
#             elif visible.name == 'products':
#                 visible.field.widget.attrs['id'] = 'id_products'

#     def save(self,child_tags={},commit=True):
#         tag = super(AddProductTags,self).save(commit=False)

#         if commit:

#             if child_tags:
#                 for child_tag in child_tags:
#                     child_tag.tag = tag.tag
#                     child_tag.description = tag.description
#                     child_tag.save()
#             tag.save() 
#             self.save_m2m()
#         return tag

    

class AddProductTagPhysician(AddProductTags):
    class Meta:
        fields = ['products']



    
    

    
        