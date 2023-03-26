from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from medical.models import Hospital2
from django.core.exceptions import ValidationError
from pproducts.models import ProductTags
from .models import quickStartPhysician, quickStartHospital1 as quickStartHospital
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

value = "foo.bar@baz.qux"

try:
    validate_email(value)
except ValidationError as e:
    print("bad email, details:", e)
else:
    print("good email")

class ImageForm(forms.Form):
    image = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class':'form-control','id':'formFile'}))

class QuickStartHospitalInvite(ModelForm):

    hospital_name = forms.CharField(label="Hospital Name",required=True)
    email = forms.CharField(required=True)
    phone = forms.CharField(required=False,max_length=12,min_length=10)
    hospital_zip = forms.CharField(required=False,max_length=5, label='Hospital Zip')
    first_name = forms.CharField(widget=forms.TextInput(attrs={}),label="First Name",required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={}),label="Last Name",required=False)
    additional = forms.CharField(widget=forms.TextInput(attrs={}),label="Notes",required=False)

    
    class Meta:
        model = quickStartHospital
        fields = ['hospital_name','email','hospital_zip','phone','first_name','last_name','additional']
        # fields = [ 'first_name','last_name','email','phone','hospital_name','hospital_zip','additional']
        
        required_fields = ['hospital_name','email']

        widgets = {

            'hospital_name': forms.TextInput(attrs={}),
            'hospital_zip': forms.TextInput(attrs={}),
            'first_name': forms.TextInput(attrs={}),
            'last_name': forms.TextInput(attrs={}),
            'email': forms.EmailInput(attrs={}),
            'phone': forms.TextInput(attrs={}),
            'additional': forms.Textarea(attrs={})

        }

        errors = {
            'phone': {
                'max_length': "Please input no more than 12 characters in the format XXX-XXX-XXXX. Dashes may or may not be included.",
                'min_length': "Please input at least 10 characters in the format XXX-XXX-XXXX. Dashes may or may not be included."
            }
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self,*args,**kwargs):
        
        hospital_name = self.cleaned_data.get('hospital_name','')
        hospital_email = self.cleaned_data.get('email','')

        notUnique = quickStartHospital.objects.filter(hospital_name=hospital_name,email=hospital_email)

        if notUnique:
            raise ValidationError(message=f"A Hospital already exists with the name {hospital_name} and zip {hospital_email}")
        cleaned = super().clean(*args,**kwargs)

        return cleaned

    def clean_email(self):
        email = self.cleaned_data.get('email','')
        try:
            validate_email(email)
        except ValidationError as e:
            raise ValidationError("Please enter a valid Email Address.")
       
        return email
            
    def clean_phone(self):
        phone = self.cleaned_data.get('phone','')
        if phone:
            result = re.match(pattern=r'^[0-9]{3}-?[0-9]{3}-?[0-9]{4}$',string=phone)
            print('result',result)

            if result is None:
                print("right hereeeeeeeeeeee")
                raise ValidationError(message="Please input a ten digit telephone number with or without dashes. I.E XXX-XXX-XXXX or XXXXXXXXXX")
        
        return phone
 
class QuickStartPhysicianForm(ModelForm):

    # hospitals = forms.ModelChoiceField(widget=forms.Select(attrs={'onchange':'populateName(event)'}), queryset=Hospital2.objects.all(),required=False)
    # test = forms.CharField(widget=forms.TextInput,max_length=20,min_length=2)
    # first_name = forms.CharField(max_length=50,required=True, min_length=2)
    # last_name = forms.CharField(max_length=50,required=True, min_length=2)
    # email = forms.EmailField(max_length=40,min_length=7,required=True)
    # specialty = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'select-specialty'}),queryset=ProductTags.objects.all().order_by('tag'))
    EMAIL_OPTIONS = [
        ('none','Please Select Option'),
        (0, "Default"),
        (1, 'Custom')
    ]
    CHOICES = [
        ('','Please Select'),
        ('new','New Hospital'),
        ('invite', 'Recently Invited'),
        ('onboarded','Fully Onboarded'),
        ('na', 'Don\'t Assign')
    ]
    hospital_list = list(Hospital2.objects.all().values_list('id','name'))
    hospital_list.insert(0,('','New Hospital'))
    hospital_type = forms.ChoiceField(label="Hospital Type",widget=forms.Select(attrs={'onchange':'populateSelections(event)'}),choices=CHOICES,required=False)
    # hospital_type = forms.ChoiceField(widget=forms.Select(attrs={'onchange':'populateFields(event)'}),required=False)
    email_options = forms.ChoiceField(widget=forms.Select(attrs={'id': 'email_options', 'onchange': 'buildEmailFields(event)',}),choices=EMAIL_OPTIONS,required=False)
    hospital = forms.ModelChoiceField(queryset=Hospital2.objects.all().order_by('name'),widget=forms.Select(attrs={'onchange':'populateName(event)','id':'hospitalModelField'}),required=False)
    hospital_invite = forms.ModelChoiceField(label="Recently Invited",queryset=quickStartHospital.objects.all().exclude(is_registered=True).order_by('hospital_name'),widget=forms.Select(attrs={'id':'hospitalInvite'}),required=False)
    hospital_name = forms.CharField(label="Hospital Name",widget=forms.TextInput(attrs={'id':'hospitalNameBox'}),max_length=50,required=False, min_length=2)
    hospital_email = forms.EmailField(label="Contact Email",max_length=40,widget=forms.EmailInput(attrs={'id':'newHospitalZip','name':'hospitalZip',}),required=False)
    # hospital_type = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:40vw;'}),choices=CHOICES)
    email_message = forms.CharField(widget=forms.Textarea(attrs={'id':'emailmessagebox','rows':'5','cols':'20','style':'display:none;'}),required=False)
    class Meta:
        model = quickStartPhysician
        fields = ['hospital_type','hospital','hospital_invite','hospital_name','hospital_email','first_name','last_name','email','specialty','email_options','email_message']
        error_messages = {
            'email': {
                'required':'Required',
                'invalid': 'Please Enter Email Address in the correct format.'
            }
        }
        # widgets = {
        #     'hospital_type': forms.Select(attrs={'onchange': 'populateSelections(event)','id':'testthisbitch'})
        # }
        labels = {
            'hospital_type': 'Hospital Type'
        }
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for visible in self.visible_fields():
            if visible.name != 'hospital_type':
                visible.field.widget.attrs['class'] = 'form-control'
            if visible.name == 'specialty':
                visible.field.widget.attrs['style'] = 'margin-top:10vh;'

            
    
    def save(self,commit = True):
        qs_physician = super().save(commit=False)
        if commit:
            # qs_physician.save_no_history()
            # if qs_physician.hospital_type == 'new' and qs_physician.hospital_name and hospital_email:
            #     qs_physician.hospital_invite = quickStartHospital.objects.create(hospital_name=qs_physician.hospital_name,hospital_zip=hospital_email)
            qs_physician.save()
            self.save_m2m()
        return qs_physician
    
    def clean(self, *args, **kwargs):
        hospital_type = self.cleaned_data.get('hospital_type','')
        hospitals = self.cleaned_data.get('hospital','')
        hospital_name = self.cleaned_data.get('hospital_name','')
        hospital_invite = self.cleaned_data.get('hospital_invite','')
        hospital_email = self.cleaned_data.get('hospital_email','')
        
        # if not hospitals and not hospital_name:
        #     raise ValidationError("If an existing hospital is not selected please input a Hospital Name. This can be edited later.")
        if hospital_type == 'new' and (not hospital_name or not hospital_email):
            raise ValidationError("If a quick starting a physician for a new hospital please input both the hospital name and email.")
        elif hospital_type == 'onboarded' and not hospitals: 
            raise ValidationError("If a quick starting a physician for a onboarded hospital please select from the list of previously onboarded hospitals.")
        elif hospital_type == 'invite' and not hospital_invite:
            raise ValidationError("If a quick starting a physician for a recently invited hospital please select from the list of previously invited hospitals.")
        # else:
        #     qset = quickStartHospital.objects.filter(hospital_zip=hospital_zip,hospital_name=hospital_name)
        #     if qset:
        #         pass
        #     print("right hereeeeeeee")
        self.checkUniqueNameAndZip(hospital_name=hospital_name,hospital_zip=hospital_email)
        cleaned = super().clean(*args,**kwargs)
        return cleaned

    
    def clean_zip(self):
        hospital_zip = self.cleaned_data.get('hospital_zip','')
        match = re.match(pattern=r'^\d{5}$',string=hospital_zip)
        if not match:
            raise ValidationError("Please make sure the zipcode is 5 numeric digits.")
        return hospital_zip
    
    def checkUniqueNameAndZip(self,hospital_name='',hospital_zip=''):
        qset = quickStartHospital.objects.filter(hospital_name=hospital_name,hospital_zip=hospital_zip)
        if qset:
            raise ValidationError(f"There is already a facility who has been previously invited with the name {hospital_name} and zip code {hospital_zip}")
        
class quickStartPhysicianSimple(ModelForm):

    class Meta:
        model = quickStartPhysician
        fields = ['first_name','last_name','email','specialty',]
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for visible in self.visible_fields():
            if visible.name != 'hospital_type':
                visible.field.widget.attrs['class'] = 'form-control'
            if visible.name == 'specialty':
                visible.field.widget.attrs['style'] = 'margin-top:10vh;'


