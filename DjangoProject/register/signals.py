from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from login.models import userProfileAdmin


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = userProfileAdmin.objects.create(user=instance)
        profile.save()
        instance.userprofileadmin.save()

