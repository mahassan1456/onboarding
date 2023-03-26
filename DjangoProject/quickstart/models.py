from django.db import models
from django.utils import timezone
from django.core.validators import validate_email, EmailValidator, MinLengthValidator, MaxLengthValidator, RegexValidator
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from django.forms.models import model_to_dict 
from pproducts.fields import MyJsonField
from pproducts.models import Physician
from .utility_functions import user_directory_path_QS_physicians
from pproducts.models import ProductTags
from superuseractions.models import QuickInviteLogs


class quickStartHospital1(models.Model):    
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE,related_name='qs_hospital')
    hospital_name = models.CharField(max_length=50,blank=True,null=False,default="")
    hospital_zip = models.CharField(max_length=40,null=True,default="")
    hospital_address = models.CharField(max_length=60,null=True, default="")
    first_name = models.CharField(null=True,max_length=50,blank=True,default="",validators=[MinLengthValidator(limit_value=2,message="This field must have a minimum of 2 characters")])
    last_name = models.CharField(max_length=50,null=True,blank=True,default="",validators=[MinLengthValidator(limit_value=2,message="This field must have a minimum of 2 characters")])
    email = models.EmailField(max_length=50,blank=True,null=True,default="")
    soft_delete = models.BooleanField(default=False)
    phone = models.CharField(max_length=12,null=True,default="",blank=True)
    additional = models.TextField(max_length=250,default="",blank=True)
    email_message = models.TextField(max_length=512,default="")
    is_emailed = models.BooleanField(default=False)
    has_physicians = models.BooleanField(default=False)  
    is_registered = models.BooleanField(default=False)
    number_emails_sent = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now, null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True,blank=True)

    


    def returnCreatedAt(self):
        return self.created_at.strftime('%B %d, %Y %I:%M %p')
    
    def returnUpdatedAt(self):
        return self.updated_at.strftime('%B %d, %Y %I:%M %p')
    
    def getIsEmailed(self):
        if self.is_emailed:
            return "Invited"
        return ""

    def getIsRegistered(self):
        if self.is_registered:
            return "Registered"
        return ""
    
    def getHasPhysicians(self):
        if self.has_physicians:
            return "Physicians"
        return ""

    def isComplete(self):
        if self.is_emailed and self.is_registered:
            return True
        return False

    def getStatus(self):
        if self.is_emailed:
            if self.is_registered:
                if self.has_physicians:
                        return 'Registration Complete'
                return "Registered / Not Recommending "
            elif self.has_physicians:
                return "Not Registered /Recommending "
            return "Invited / Not Registered"
        return "Not Registered / Not Invited"
    def colorCode(self):
        if self.is_registered:
            return "green"
        return "red"

    def get_full_name(self):
        full_name = f"{self.first_name.strip()} {self.last_name.strip()}"
        return full_name.strip() if full_name.strip() else "Not Provided"
    def getEmail(self):
        if self.email:
            return self.email
        return "Not Assigned"

    def get_full_address(self):
        return f"{self}"

    def __str__(self):
        return f"{self.hospital_name.title()}"  
    
    def onboardPhysicians(self,hospital=''):
       onboarded_physician_set = self.qs_physicians.filter(is_assigned=True,is_onboarded=True,is_recommending=True)

       for qs_physician in onboarded_physician_set:
           Physician.objects.create(firstName=qs_physician.first_name,lastName=qs_physician.last_name,email=qs_physician.email,specialty_ph=qs_physician.specialty.all(),)
    

class quickStartPhysician(models.Model):

    CHOICES = [
        ('new','New Hospital'),
        ('invite', 'Recently Invited'),
        ('onboarded','Fully Onboarded'),
        ('na', 'Don\'t Assign')
    ]

    hospital = models.ForeignKey(to='medical.Hospital2',on_delete=models.CASCADE,null=True,blank=True,related_name="qsp")
    hospital_invite = models.ForeignKey(to=quickStartHospital1,on_delete=models.CASCADE,null=True,blank=True,related_name='qs_physicians')
    hospital_type = models.CharField(max_length=25,choices=CHOICES,default="",blank=True)
    hospital_name = models.CharField(max_length=50,blank=True,null=False,default="")
    first_name = models.CharField(max_length=50,blank=False,default="",validators=[MinLengthValidator(limit_value=2,message="This field must have a minimum of 2 characters")])
    last_name = models.CharField(max_length=50,blank=False,default="")
    email = models.EmailField(max_length=50,blank=False)
    specialty = models.ManyToManyField(to='pproducts.ProductTags',null=True)
    date_created = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now, null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True,blank=True)
    # products = models.ManyToManyField(to="pproducts.Product", null=True, default=None)
    email_message = models.TextField(max_length=512, default="")
    picture = models.ImageField(upload_to=user_directory_path_QS_physicians, null=True,blank=True)
    description = models.TextField(max_length=512,default='')
    # For a Invited Physician to become an Onboarded Physician. all three fields below must be set to True.
    is_assigned = models.BooleanField(default=False)
    is_emailed = models.BooleanField(default=False)
    is_onboarded = models.BooleanField(default=False)
    is_recommending= models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    products = MyJsonField(null=True,blank=True)
    # history = HistoricalRecords()
    about_me = models.TextField(max_length=512,default="")

    def returnCreatedAt(self):
        return self.created_at.strftime('%B %d, %Y %I:%M %p')
    
    def returnUpdatedAt(self):
        return self.updated_at.strftime('%B %d, %Y %I:%M %p')
    
    def logRecord(self,email_options='',user=''):
        qsl = QuickInviteLogs.objects.create(email=self.email,entity_name=self.getHospitalName(),entity_type="physician",message=int(email_options),action="Quick Invite(Physician)")
        qsl.user = user
        qsl.save()

    def isComplete_(self):
        if self.is_emailed and self.is_onboarded and self.is_recommending:
            return True
        return False


    def needsReminder(self):
        if not self.is_recommending:
            return True
        return False
    def needsReminderString(self):
        if not self.is_recommending:
            return "Send Reminder"
        return "Recommending"
    def convertToOnboarded(self,post={}):
        try:
            data = {
                        'firstName': self.first_name,
                        'lastName':self.last_name,
                        'picture':self.picture,
                        'description': self.description,
                        'email': self.email,
                        'products':self.products,
                        'about_me':self.about_me
                    }
            print(data)
            
            return data
        except Exception as error:
            print(error)
            return ''

    def setState(self):
        
        if self.is_recommending and self.is_onboarded:
            self.is_complete = True
        if self.hospital_name:
            self.is_new = True
        if self.hospital_name or self.hospital or self.hospital_invite:
            self.is_assigned = True
        if self.hospital:
            self.is_onboarded = True
        if self.products:
            self.is_recommending = True
        
        self.save()
    def getIsEmailed(self):
        if self.is_emailed:
            return "Emailed"
        return ""
    def getIsRecommending(self):
        if self.is_recommending:
            return "Recommending"
        return ""
    def getIsOnboarded(self):
        if self.is_onboarded:
            return "Onboarded"
        return ""
    

    def getHospitalName(self):
        if self.hospital:
            return self.hospital.name.title()
        elif self.hospital_invite:
            return self.hospital_invite.hospital_name.title()
        elif self.hospital_name:
            return self.hospital_name.title()
        else:
            return "Hospital Not Assigned"
    
    def getStatus(self):
        statusString = ''
        choices = ['is_emailed','is_assigned','is_recommending']
        if self.is_complete:
            return "Complete"
       
        for i,choice in enumerate(choices):
            title = choice.split('_')[1].title()
            result = title if getattr(self,choice) else f"Not {title}"
            statusString = statusString + ' ' + result
            if i != len(choices)-1:
                 statusString += '/'

        return statusString
        
    def save(self, *args,**kwargs):
    
        super(quickStartPhysician, self).save(*args, **kwargs)
    def getEmail(self):

        if self.email:
            return self.email
        return "Not Provided"

    def save_no_history(self, *args, **kwargs):
        self.skip_history_when_saving = True
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret
    def buildProductsString(self):
        string_holder = []
        string = 'You are currently Recommending the Specialty '
       
        for specialty,products in self.products.items():
            string += specialty.title()
            for index,product in enumerate(products):
                if index == 0:
                    string += f" w/ the following Products: {index+1}.{product}\n"
                    
                else:
                    if index != len(products) - 1:
                        string += f" {index+1}.{product}\n"
                    else:
                        string += f" {index+1}.{product}.\n"
            
            string_holder.append(string)
            string = 'Recommending the Specialty '
        
        return '\n'.join(string_holder)

    def buildProductsQuick(self,data={}):
        try:
            products = { key.split('-')[0]:data.getlist(key) for key in data.keys() if "-" in key}
            if len(products):
                self.is_recommending = True
                self.products = products
                picture = data.get('picture','')
                self.picture = picture
                selections = ProductTags.objects.filter(id__in=data.getlist('selections'))
                print(selections)
                self.specialty.add(*selections)
                self.description = data.getlist('about_physician')[0]
                self.save()
        except Exception as error:
            print(error)
            return error
        print("returning this shit")
        return products

    def get_full_name(self):
        full_name = f"{self.first_name.title()} {self.last_name.title()}"
        if full_name:
            return full_name
        return "Not Provided"
    def __str__(self):
        return f"{self.first_name.title()} {self.last_name.title()}"
    def buildSpecialtyString(self):
        return ", ".join(list(map(lambda x: x.tag, list(self.specialty.all()))))
    def buildCSV(self):
        return ", ".join(list(map(lambda x: x.tag, list(self.specialty.all()))))
    
    
    
    

    
    
    

