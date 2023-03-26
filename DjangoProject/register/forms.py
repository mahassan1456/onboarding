from django import forms
from django.forms import ModelForm
from medical.models import Hospital2 as HP
from medical.arrays import STATES, COMMON_DOMAINS_LIST
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import validate_email, EmailValidator, MinLengthValidator, MaxLengthValidator, RegexValidator
from django.contrib.auth.password_validation import CommonPasswordValidator
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.core.mail import send_mail, BadHeaderError
import time
from quickstart.models import quickStartHospital1 as quickStartHospital
from pproducts.models import Physician,ProductTags
from pproducts.forms import AddPhysicianAdmin
from medical.forms import AddHospital as AH




class PhysicianForm(AddPhysicianAdmin):
    
    specialty_ph = forms.ModelMultipleChoiceField(required=False,label="Specialty Areas",widget=forms.CheckboxSelectMultiple(attrs={'onchange':'refreshProducts23(event)','id':'formFile'}), queryset=ProductTags.objects.all().order_by('tag'))
    about_me = forms.CharField(widget=forms.Textarea(attrs={'rows':7,'cols':50,'id':'about_physician',}))

    class Meta:
        model = Physician
        fields = ['picture','about_me','firstName','lastName','email','specialty_ph']

    def __init__(self, *args,fields=[], **kwargs):

        super().__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

def customPasswordValidator(password1,password2):

    if password1 == password2:
        return False
    return True

class AddHospitalForm(AH):
    admin_name = forms.CharField(label='Admin Name',max_length=50,required=True,widget=forms.TextInput(attrs={}))
    is_manual = forms.BooleanField(label="",required=False,widget=forms.HiddenInput(attrs={}))
    prompt_credentials = forms.BooleanField(label="",required=False,widget=forms.HiddenInput(attrs={}))

    class Meta:
        model = HP
        fields = ['is_manual','prompt_credentials','picture','id','name','admin_name','taxid','bankaccount','routing','street','city','state','email','zip','phone','website','total_physicians']

    
        

class AddHospital(ModelForm):
    picture = forms.ImageField(required=False,widget=forms.FileInput(attrs={'id':'formField'}))
    name = forms.CharField(label="Facility Name: ",min_length=2,max_length=50,required=True, widget=forms.TextInput(attrs={'id':'hspname','placeholder':'Enter Hospital Name','autofocus':'true','required':'true','id':'input1'}))
    taxid = forms.CharField(required=True,label="Tax ID: ",max_length=10,min_length=9,widget=forms.TextInput(attrs={'placeholder':'Enter Tax ID e.g 12-9434553','id':'input2','name':'Tax ID'}), 
        error_messages={'unique':"Tax ID Already Exists.If this has occurred in error please email the administrator. "})
    bankaccount = forms.CharField(label="Bank Account #: ",min_length=5,max_length=17,widget=forms.TextInput(attrs={'class':'form-input', 'placeholder':'Enter 9-20 digit bank account','id':'input3'}),required=True)
    routing = forms.CharField(label="Routing #: ",max_length=9,min_length=9,widget=forms.TextInput(attrs={'class':'form-input','placeholder':'Enter 9 Digit Routing','id':'input4','name':'routing'}),required=True)
    street = forms.CharField(label="Street: ",max_length=50,widget=forms.TextInput(attrs={'id':'toggle','id':'input5','placeholder': 'Enter Street Name'}),required=True)
    city = forms.CharField(label="City: ",max_length=50,widget=forms.TextInput(attrs={'id':'toggle1','name':'City','id':'input6', 'placeholder':'Enter a City'}),required=True)
    state = forms.Select(attrs={'class':'form-input','id':'is_staff_user22','id':'id_state','required':False,'name':'state'})
    zip = forms.CharField(label="Zip: ",max_length=5,min_length=5,widget=forms.TextInput(attrs={'name':'zip','id':'is_super_user1','id':'input8','placeholder':'Enter 5 digit Postal Code'}),required=False)
    email = forms.EmailField(max_length=60,min_length=5,required=True)
    phone = forms.CharField(max_length=12,min_length=10,required=True)
    website = forms.CharField(label="Website: ",min_length=4,widget=forms.TextInput(attrs={'id':'is_super_user2','id':'input9','placeholder':'Enter Website e.g www.google.com'}),required=True)
    
    total_physicians = forms.IntegerField(label="Total Physicians: ",widget =forms.NumberInput(attrs={'name':'Total Physicians','id':'is_super_user3','id':'input10','placeholder': 'Total Number of Physicians','required':False}))

    class Meta:
        model = HP
        fields = ['picture','id','name','admin_name','taxid','bankaccount','routing','street','city','state','zip','email','phone','website','total_physicians']

        labels = {

            'name': 'Hospital Name *',
            'taxid': 'Tax ID *',
            'bankaccount': 'Bank Account *',
            'routing': 'Routing *',
            'street': 'Street *',
            'city': 'City *',
            'state': 'State *',
            'zip': 'Zip *',
            'website': 'Website *',
            'total_physicians *': 'Total Physicians *'
        }
        

    def __init__(self, *args,fields=[], **kwargs):

        super().__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self, *args, **kwargs):

        taxid = self.cleaned_data.get('taxid','')
        notUniqueTaxID = HP.objects.filter(taxid=taxid)
        if notUniqueTaxID:
            raise ValidationError("The Tax ID is already registered. If you have received this message in error please contact the administrator.")
        bankaccount = self.cleaned_data.get('bankaccount','')
        notUniqueBankAccount = HP.objects.filter(bankaccount=bankaccount)
        if notUniqueBankAccount:
            raise ValidationError("The Bank Account No is already in use. If you have received this message in error please contact the administrator.")
        street = self.cleaned_data.get('bankaccount','')
        city = self.cleaned_data.get('city','')
        state = self.cleaned_data.get('state','')
        zip = self.cleaned_data.get('zip','')
        notUniqueAddress = HP.objects.filter(street=street,state=state,zip=zip,city=city)
        if notUniqueAddress:
            raise ValidationError("The address is already in use. Please check the address and try again. If you have received this message in error please contact the administrator at xxx@xxx.com")
        cleaned = super().clean(*args,**kwargs)
        return cleaned

    def clean_taxid(self):
        taxid = self.cleaned_data.get('taxid','')
       
        result = re.match(pattern=r'^(\d){2}(-)?(\d){7}$',string=taxid)
        if not result:
            raise ValidationError("Invalid Format.The tax id should be 9 digits and provided in the format ##-#######")
        if taxid[2] == "-":
            taxid = "".join(taxid.split('-'))
        
        return taxid
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone','')
        if phone:
            result = re.match(pattern=r'^[0-9]{3}-?[0-9]{3}-?[0-9]{4}$',string=phone)
            print('result',result)

            if result is None:
                print("right hereeeeeeeeeeee")
                raise ValidationError(message="Please input a ten digit telephone number with or without dashes. I.E XXX-XXX-XXXX or XXXXXXXXXX")
        
        return phone

    def clean_bankaccount(self):
        bankaccount = self.cleaned_data.get('bankaccount','')
        result = re.match(pattern=r'^(\d){5,17}$', string=bankaccount)

        if not result:
            raise ValidationError("Bank account # is a numeric value consisting of 5-17 digits.")
        
        return bankaccount

    def clean_routing(self):
        routing = self.cleaned_data.get('routing','')
        result = re.match(pattern=r'^(\d){9}$', string=routing)

        if not result:
            raise ValidationError("The routing number is a 9 digit numeric value.")
        return routing

    def clean_city(self):
        city = self.cleaned_data.get('city','')
        result = re.match(pattern=r'^[A-Za-z- ]{2,}$', string=city)

        if not result:
            raise ValidationError("Invalid Format.")
        return city

    def clean_state(self):
        state = self.cleaned_data.get('state','')
        if state:
            state = state.upper()
            return state
        else:
            return "N/A"

    def clean_zip(self):
        zip = self.cleaned_data.get('zip','')
        result = re.match(pattern=r'(\d){5}', string=zip)

        if not result:
            raise ValidationError("Please input 5 digits for the zip code.")
    
        return zip

    def clean_website(self):
        website = self.cleaned_data.get('website','N/A')
        result = re.match(pattern=r'www\.(\w){2,}\.[A-Za-z]{3}$', string=website)
        if not result:
            raise ValidationError("Please input website in the correct format beginning with www and ending with a three letter domain e.g gov,com,net")
        return website
    

# class QuickStartHospitalInvite(ModelForm):


#     class Meta:
#         model = quickStartHospital
#         fields = [ 'hospital_name','hospital_zip','first_name','last_name','email','phone','additional']
#         widgets = {

#             'hospital_name': forms.TextInput(attrs={}),
#             'hospital_zip': forms.TextInput(attrs={}),
#             'first_name': forms.TextInput(attrs={}),
#             'last_name': forms.TextInput(attrs={}),
#             'email': forms.EmailInput(attrs={}),
#             'phone': forms.TextInput(attrs={}),
#             'additional': forms.Textarea(attrs={})

#         }

#         def clean(self,*args,**kwargs):

#             hospital_name = self.cleaned_data.get('hospital_name','')
#             hospital_zip = self.cleaned_data.get('hospital_zip','')

#             notUnique = quickStartHospital.objects.filter(hospital_name=hospital_name,hospital_zip=hospital_zip)

#             if notUnique:
#                 return ValidationError(message=f"A Hospital already exists with the name {hospital_name} and zip {hospital_zip}")
#             cleaned = super().clean(*args,**kwargs)

#             return cleaned
        
#         def clean_email(self):
#             pass

#         def clean_phone(self):
#             phone = self.cleaned_data.get('phone')
#             result = re.match(pattern=r'^[0-9]{3}-?[0-9]{3}-?[0-9]{4}$',string=phone)

#             if result is None:
#                 return ValidationError(message="Please input a ten digit telephone number with or without dashes. I.E XXX-XXX-XXXX or XXXXXXXXXX")
            
#             return phone


class CredentialsForm(UserCreationForm):

    #########################
    first_name = forms.CharField(label='First Name *',min_length=2,widget=forms.TextInput(attrs={'id':'hspname1', 'class':'form-elements','placeholder':'First Name','autofocus':True, 'required':True}), 
    validators=[RegexValidator(regex='[a-zA-Z]+',message="Names should not Contain Numbers")], error_messages={'required': 'Please Enter Your First Name '})
    #########################

    last_name = forms.CharField(label="Last Name *",min_length=2,widget=forms.TextInput(attrs={'id':'hspname1', 'class':'form-elements','placeholder':'Last Name','autofocus':True, 'required':True}), 
    validators=[MinLengthValidator(limit_value=2,  message="Last Name must be Greater than 1 Character in Length."),
    RegexValidator(regex='[a-zA-Z]+',message="Last Names should not Contain Numbers")],error_messages={'required': 'Please Enter a Last Name'})

    email = forms.EmailField(label="Email *" ,widget=forms.EmailInput(attrs={'class':'form-elements','placeholder':'Email', 'required': True}), 
    validators=[],error_messages={'required': 'Please Enter an Email Address: '} )

    password1= forms.CharField(min_length=8,max_length=16,
    widget=forms.PasswordInput(attrs={'class':'form-elements', 'required': True}), label='Enter A Password  *', error_messages={'required': 'Please Enter a Password: '})

    password2= forms.CharField(min_length=8, max_length=16,
    widget=forms.PasswordInput(attrs={'class':'form-elements', 'required': True}), label='Re-enter Password *', error_messages={'required': 'Please Verify your Password. '})

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1","password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args,**kwargs)
        
        return cleaned_data

    def clean_email(self,*args,**kwargs):
        email = self.cleaned_data.get('email')
        domain = email.split('@')[1].split('.')[0]
        email_object = User.objects.filter(email=email)

        if email_object:
            raise ValidationError("Email Already Exists")

        if domain in COMMON_DOMAINS_LIST:
            raise ValidationError("Please Enter a Corporate Email Domain.")

        return email
    
    def clean_username(self,*args,**kwargs):
        username = self.cleaned_data.get('username')
        username_object = User.objects.filter(username=username)

        if username_object:
            raise ValidationError("Username already Exists")

        result = re.match(pattern=r'[a-zA-Z]+[a-zA-Z0-9]{8,20}', string='allanjames24')

        if not result:
            raise ValidationError("Username already exists. Please select a unique username up to 20 characters long.")

        return username
        
    def clean_password2(self,*args,**kwargs):
        password1 = self.cleaned_data.get('password1', False)
        password2 = self.cleaned_data.get('password2', False)

        if password1 and password2:
            password_validate_result = customPasswordValidator(password1=password1,password2=password2)

            if password_validate_result:
                raise ValidationError("Please Input a Matching Password with the minimum complexity requirements.")

            result = re.match(pattern=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{8,16}$',string=password2)
            if not result:
                raise ValidationError("Password must be a Minimum eight to sixteen characters, at least one letter and one number")

        return password2
        
    def clean_password1(self,*args,**kwargs):
        password = self.cleaned_data.get('password1', False) 
        password2 = self.cleaned_data.get('password2', False)

        if password and password2:
            password_validate_result = customPasswordValidator(password1=password,password2=password2)

            if password_validate_result:
                raise ValidationError("Please Input a Matching Password with the minimum complexity requirements."
            )
            result = re.match(pattern=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{8,16}$',string=password)
            
            if not result:
                raise ValidationError("Password must be a Minimum eight to sixteen characters, at least one letter and one number")

        return password

class CredentialsFormAdmin(CredentialsForm):
    
    facility = forms.ModelChoiceField(label='Hospital',required=True,queryset=HP.objects.all().order_by('name'),widget=forms.Select(attrs={'id':'hospitalsbox','name':'hospitals','data-tbl':'hospital2user'}))
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['facility','first_name','last_name','email','username','password1','password2']

class Login(forms.Form):
    username = forms.CharField(required=True, label="Username", widget=forms.TextInput(attrs={'name':'username','class':'form-control icon_gap','id': 'validationCustom01','placeholder':'User Name','required':True,
    'required':'true'}))
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'name':'password','placeholder':'Please enter a password.','required':True,'required':'true','class':'form-control icon_gap','id':'validationCustom02'}))
    class Meta:
        fields = ['username','password']
    
class ApproveFromLogin(Login):
  
    class Meta(Login.Meta):
        exclude = []


class ContactForm(forms.Form):
    firstname = forms.CharField(label="First Name",max_length = 50, required=True)
    lastname = forms.CharField(label="Last Name",max_length = 50,required=True)
    emailaddress = forms.EmailField(label="Email Address",max_length = 150, required=True)
    message = forms.CharField(label="Message",widget = forms.Textarea(attrs={'class':'messagebox'}), max_length = 2000, required=True)
   
    def clean_firstname(self):
        pass
    def clean_lastname(self):
        pass
    def clean_emailaddress(self):
        pass
    def clean_message(self):
        pass

# class QuickInviteAddHospital(AddHospital):

#     first_name = forms.CharField(max_length=40,min_length=3,widget=forms.TextInput(attrs={}))
#     last_name = forms.CharField(max_length=40,min_length=3,widget=forms.TextInput(attrs={}))
#     email = forms.EmailField(max_length=40,required=True,widget=forms.EmailInput(attrs={}))
#     phone = forms.CharField(max_length=12,min_length=12,required=False,widget=forms.TextInput(attrs={}))

#     class Meta:
#         model = HP
#         # fields = ['picture','taxid','bankaccount','routing','street','city','state','zip', 'website','total_physicians']
#         # fields = ['name','full_name','email','phone','picture','taxid','bankaccount','routing','website','total_physicians']
#         fields = ['name','zip','first_name','last_name','email','phone']

#         labels = {

#             'name': 'Hospital Name *',
#             'zip': 'Full Name',
#             'email': 'E-Mail',
#             'phone':'Phone',
#             'taxid': 'Tax ID *',
#             'bankaccount': 'Bank Account *',
#             'routing': 'Routing *',
#             # 'street': 'Street *',
#             # 'city': 'City *',
#             # 'state': 'State *',
#             # 'zip': 'Zip *',
#             'website': 'Website *',
#             'total_physicians *': 'Total Physicians *'
#         }
    
#     def clean_phone(self):
#         phone = self.cleaned_data.get('phone')
#         result = re.match(pattern=r'^[0-9]{3}-?[0-9]{3}-?[0-9]{4}$',string=phone)

#         if result is None:
#             return ValidationError(message="Please input a ten digit telephone number with or without dashes. I.E XXX-XXX-XXXX or XXXXXXXXXX")
        
#         return phone

# class ContactForm(forms.Form):
    
# 	firstname = forms.CharField(max_length = 50, required=True)
# 	lastname = forms.CharField(max_length = 50,required=True)
# 	emailaddress = forms.EmailField(max_length = 150, required=True)
# 	message = forms.CharField(widget = forms.Textarea, max_length = 2000, required=True)


class EditPhysician(ModelForm):
    # specialty_ph = forms.ModelMultipleChoiceField(required=False,label="Specialty Areas",widget=forms.CheckboxSelectMultiple(attrs={'onchange':'refreshProducts23(event)','id':'formFile'}), queryset=ProductTags.objects.all().order_by('tag'))
    
    about_me = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':7,'cols':50,'id':'about_physician',}))

    class Meta:
        model = Physician
        fields = ['picture','about_me','firstName','lastName','email']
        required_fields = ['firstName']

    def __init__(self, *args,fields=[], **kwargs):

        super().__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
