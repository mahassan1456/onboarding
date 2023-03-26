

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
from medical.forms import AddHospital
from medical.models import Hospital2 as HP



class AddHospitalManual(AddHospital):
    mobile_contact = forms.CharField(widget=forms.TextInput(attrs={}),required=False)

    class Meta:
        model = HP
        fields = ['picture','id','name','taxid','bankaccount','routing','street','city','state','zip','phone','website','total_physicians']



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
    

    class AddProductTags(ModelForm):


        CHOICES = (
        ("", "Push To WooCommerce" ),
        ('create', 'New Tag(Specialty)'),
        ('update', 'Update Tag(Specialty)'),
        ("no_push", 'Do Not Push'),
)
    
        pushtowoo = forms.ChoiceField(label="",required=True,widget=forms.Select(attrs={"onchange": "populateDropDown(event)"}),choices=CHOICES)

        class Meta:
            model = ProductTags
            exclude = []

    def __init__(self, *args, **kwargs):

        super().__init__(*args,**kwargs)
        for visible in self.visible_fields():
            print(visible.name)
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