from django.db import models
from django.contrib.auth.models import User
from medical.arrays import STATES
from django.core.validators import validate_email, EmailValidator, MinLengthValidator, MaxLengthValidator, RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib import messages
from superuseractions.models import UserHistoryTable
from django.utils import timezone, dateformat
from .utility_functions import user_directory_path_hospital


class Hospital2(models.Model):
    from superuseractions.models import UserHistoryTable
    picture = models.ImageField(upload_to=user_directory_path_hospital, null=True,blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, blank=True,related_name="hospitals")
    name = models.TextField(max_length=50, null=False,default="")
    
    taxid = models.CharField(max_length=10,blank=False, null=True, default="")
    bankaccount = models.CharField(max_length=17,blank=False, null=True,default="")
    routing = models.CharField(max_length=9,null=False,default="")
    street = models.TextField(max_length=100, null=False,default="")
    city = models.TextField(max_length=50,default="")
    state = models.CharField( max_length=5, null=False, choices=STATES,blank=True,default="")
    zip = models.TextField(max_length=5, null=True,default="")
    phone = models.CharField(max_length=12,null=True,default="")
    email = models.EmailField(null=True,default="",max_length=60,blank=True)
    total_physicians = models.IntegerField(null=True,blank=True,)
    physicians_onboarded = models.IntegerField(default=0,blank=True)
    website = models.CharField(max_length=50,null=False,default="")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_manual = models.BooleanField(default=False)
    is_manual_time = models.DateTimeField(default=timezone.now,null=True)
    soft_delete = models.BooleanField(default=False)
    prompt_credentials = models.BooleanField(default=False)
    approved = models.BooleanField(null=False,default=False)
    approved_at =  models.DateTimeField(null=True,blank=True)
    approved_by = models.CharField(max_length=35,null=False,blank=True,default='')
    has_physicians = models.BooleanField(default=False)
    has_administrator = models.BooleanField(default=True)
    sd = models.BooleanField(default=False)
    sd2 = models.BooleanField(null=True)
    admin_name = models.CharField(max_length=40,default='',null=True)
    admin_name_1 = models.CharField(max_length=40,default='',null=True)
    # last_name = models.CharField(max_length=40,default='',null=True)


    def returnCreatedAt(self):
        return self.created_at.strftime('%B %d, %Y %I:%M %p')
    
    def returnUpdatedAt(self):
        return self.updated_at.strftime('%B %d, %Y %I:%M %p')

    def logRecord(self,action='',action_verbose=''):
        uht = UserHistoryTable.objects.create(action=action,entity_type="Hospital",entity_id=self.id,entity_name=self.name,action_verbose=action_verbose,page_link=f"/register/edit/hospital/{self.id}/")
        uht.user = self.user
        uht.save()
        self.save()
        return uht

        record = UserHistoryTable.objects.create(action=action,entity_type='hospital',entity_id=self.id,entity_name=self.name,)
    def __repr__(self):
        return f"Hospital <{self.name}>"
    def __str__(self):
        return f"Hospital <{self.name}>"
    
    def checkState(self,data_s=[],object_dict={},):
        action_obj = {}
        delta = False
        if data_s:
            for data in data_s:
                if data == 'picture':
                    action_obj[data] = {'prev':object_dict[data].url if object_dict.get(data,'') else '' ,'curr':getattr(self,data).url if getattr(self,data) else ''}
                else:
                    action_obj[data] = {'prev':object_dict.get(data,''),'curr':getattr(self,data)}
        return action_obj 

    def countPhysicians(self,*args,**kwargs):
        self.physicians_onboarded = self.physician_set.all().count()
        super().save(*args,**kwargs)
        return self.physicians_onboarded
    def getStatus(self):

        if self.email:
            if self.is_manual:
                return "Send Reminder"
            else:
                return "Registered/Onboarded"
        else:
            return "Send New Invite"
    def getStatusColor(self):
        if self.email:
            if self.is_manual:
                return "color:rgb(161, 161, 21)"
            else:
                return "color:green;pointer-events:none;"
        else:
            return "color:red;"


    def logHistory(self,user,created=False):
        time = dateformat.format(self.created_at, 'Y-m-d')
        if not created:
            record = self.history.latest()
            record.history_change_reason = f"{user} Updated Hospital {self.name} at {time}"
        else:
            record = self.history.latest()
            record.history_change_reason = f"{user} Created Hospital {self.name} at {time}"
        record.save()
        self.save_no_history()

    def approve(self, username):
        self.approved = True
        self.approved_at = timezone.now()
        self.approved_by = username
        self.save()

    def get_full_address(self):
        return f"{self.street} {self.city}, {self.state} {self.zip}"

    def validate_unique(self, exclude=None):
        qs = Hospital2.objects.filter(bankaccount=self.bankaccount).exclude(id=self.id)
        if qs:
            raise ValidationError('Bank Account # must be unique')
        qs = Hospital2.objects.filter(taxid=self.taxid).exclude(id=self.id)
        if qs:
            raise ValidationError("Tax ID Must be unique")

    def save(self, *args, **kwargs):
        self.validate_unique()

        super().save(*args, **kwargs)

    def save_no_history(self, *args, **kwargs):
        self.skip_history_when_saving = True
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret

    class Meta:
        ordering = ['-is_manual','-created_at'] 

