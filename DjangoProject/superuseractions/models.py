from django.db import models
from django.contrib.auth.models import User
from pproducts.fields import MyJsonField
from django.utils import timezone



class UserHistoryTable(models.Model):
    CHOICES = (
        ('1','Create'),
        ('2','Update'),
        ('0','Delete'),
        ('3','Restored'),
        ('4','Onboarded')
    )
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='ahistory')
    action_time = models.DateTimeField(default=timezone.now, null=True,blank=True)
    action = models.CharField(max_length=1,choices=CHOICES,null=False)
    action_code = models.CharField(max_length=16,null=True,default='')
    action_verbose = models.CharField(max_length=128,null=True,default='')
    entity_type = models.CharField(max_length=64,null=True,default='')
    entity_id = models.CharField(max_length=64,null=True,default='')
    entity_name = models.CharField(max_length=64,null=True,default='')
    change_type = models.CharField(max_length=32,null=True,default='')
    action_obj = MyJsonField(null=True,blank=True)
    page_link = models.CharField(null=True,default='',max_length=64)
    



    class Meta:

        ordering = ['-action_time']


    def save(self,*args,dele=False,**kwargs):
        action = ''
        if self.entity_type.title() == 'Physician':
            if not dele:
                if self.action_obj:
                    for key,value in self.action_obj.items():
                        if 'delta_' in key:
                            if value:
                                action = action + f"{value},"
                    try:
                        if action:
                            if action[-1] == ',':
                                action = action[0:-1] + " for "
                        else:
                            action += " for "
                    except IndexError as error:
                        print('hellllll',error)
                    self.action_verbose = action
        # elif self.entity_type == 'Product':
        #     action = " Product "
        # elif self.entity_type == 'Hospital':
        #     action = " Account for "
            

        # self.action_verbose = action
        super().save(*args,**kwargs)
        
    
    def returnLink(self):
        print('ffffff')
        return ''
        # if self.action_obj.get('entity_type','') == 'Physician':
        #     try:
        #         return f"/views/physician/detail/{self.action_obj['entity_id']}/"
        #     except Exception as error:
        #         print(error)
        # return ''

    def getAction(self):
        if self.action == '1':
            return 'Created'
        if self.action == '2':
            return 'Updated'
        if self.action == '0':
            return 'Deleted'
        if self.action == '4':
            return 'Onboarded'
        if self.action == '5':
            return "Recommending"
        return "Restored"
    def getHospitalName(self):
        from pproducts.models import Physician
        if self.entity_type == 'Physician':
            print(self.user)
            if self.user:
                if not self.user.is_superuser:
                    if self.user.hospitals:
                        try:
                            return self.user.hospitals.all()[0].name
                        except Exception as err:
                            print(err)
                    return ''
                    
                else:
                    try:
                        id = self.entity_id
                        if id:
                            
                            return Physician.objects.get(id=int(id)).facility.name
                    except (Physician.DoesNotExist ,Exception) as fucku:
                        print(fucku,'fffffuck')
                        return ''
            else:
                return ''
        else:
            return ''

            
    def buildRecordString(self):
        string = f"{self.getAction()} {self.action_verbose} {self.entity_name} at {self.action_time.strftime('%B %d, %Y %I:%M %p')}"
        print("string", string)
        return string
    


        # if self.entity_type == 'Physician':
        #     string += string + f" {self.action_obj['delta_products']},{self.action_obj['delta_profile']},{self.action_obj},"

        # if self.action_obj['delta_products']:
        #     string = string + ''
            
    def getUserType(self):
        if self.user.is_superuser:
            return 'Administrator'
        return 'User'
    def getDate(self):
        return self.action_time.strftime('%B %d, %Y %I:%M %p')
        return self.action_time.strftime('%-m/%-d/%Y')


class QuickInviteLogs(models.Model):
    choices = (
        (0,"Default"),
        (1,"Custom")
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    email = models.EmailField(max_length=50,default='')
    send_time = models.DateTimeField(auto_now_add=True)
    entity_name = models.CharField(max_length=25,default='')
    entity_type = models.CharField(max_length=30,default='')
    action = models.CharField(max_length=64,default="")
    message = models.IntegerField(default=0,choices=choices)
    
    class Meta:
        ordering = ['-send_time']


    def returnEmailType(self):
        if self.message == 0:
            return 'Default'
        return 'Custom'
    def getDate(self):
        return self.send_time.strftime('%B %d, %Y %I:%M %p')
    