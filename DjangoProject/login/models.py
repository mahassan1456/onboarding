from django.db import models
from django.core.validators import validate_email, EmailValidator, MinLengthValidator, MaxLengthValidator, RegexValidator
from django.contrib.auth.password_validation import CommonPasswordValidator
from django.contrib.auth.models import User
from login.utility_functions import user_profile_picture_directory_path
from simple_history.models import HistoricalRecords
from medical.arrays import STATES
from django.utils import timezone
from medical.models import Hospital2
from django.forms.models import model_to_dict 

class userProfileAdmin(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=user_profile_picture_directory_path,null=True,blank=True)
    mobile_contact = models.CharField(max_length=12, null=True, default="",blank=False,
        validators=[MinLengthValidator(limit_value=10, message="Please Input a value between 10 and 13 digits(if formatted w/ dashes)"),MaxLengthValidator(limit_value=13,message="Please Input a value between 10 and 13 digits(if formatted w/ dashes")])
    job_title = models.CharField(max_length=40, null=True, default="", validators=[MinLengthValidator(limit_value=2, message="Please input a Position of at least 2 chracters")])
    additional_information = models.TextField(max_length=250, null=False, default=" ",blank=True)
    prompt_credentials = models.BooleanField(default=False)
    history = HistoricalRecords()

class WaitingRoom(models.Model):
    name = models.TextField(max_length=50, null=False,default="")
    taxid = models.CharField(max_length=10,blank=False, null=True, default="")
    bankaccount = models.CharField(max_length=17,blank=False, null=True,default="")
    routing = models.CharField(max_length=9,null=False,default="")
    street = models.TextField(max_length=100, null=False,default="")
    city = models.TextField(max_length=50,default="")
    state = models.CharField( max_length=5, null=False, choices=STATES,blank=True,default="")
    zip = models.TextField(max_length=12, null=False,default="")
    total_physicians = models.IntegerField(null=True,blank=True,)
    website = models.CharField(max_length=50,null=False,default="")
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(null=False,default=False)
    approved_at =  models.DateTimeField(null=True,blank=True)
    approved_by = models.CharField(max_length=35,null=False,blank=True,default='')
    history = HistoricalRecords()

    def moveToApproved(self,approved=True,name='administrator'):
        modelDict = model_to_dict(self)
        modelDict.pop('id')
        hospital = Hospital2(**modelDict)
        hospital.approved = True
        hospital.approved_by = name
        hospital.save()
       
        return hospital
    
