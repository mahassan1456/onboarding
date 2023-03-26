from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from pproducts.models import Physician

from medical.utility_functions import *


@receiver(post_save, sender=Physician)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        pass
        
        
    


    


