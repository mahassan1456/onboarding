# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from medical.models import userProfile as UP, Hospital2


# # @receiver(post_save, sender=User)
# # def create_user_profile(sender, instance, created, **kwargs):
# #     if created:
# #         UP.objects.create(user=instance)

# # @receiver(post_save,sender=User)
# # def save_user_profile(sender,instance,created,**kwargs):
# #     if created:
# #         instance.userprofile.save()

# @receiver(post_save, sender=Hospital2)
# def saveTempGenericUser(sender,instance,created, **kwargs):
#     x=12
#     if created:
#         if instance.user is None:
#             generic_user = User.objects.get(username="unassigned")
#             generic_user.hospitals.add(instance) 
#             generic_user.save()
#             instance.save()
