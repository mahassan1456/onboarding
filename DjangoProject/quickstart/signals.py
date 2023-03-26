# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from medical.models import userProfile as UP, Hospital2
# from .models import quickStartHospital1 as quickStartHospital, quickStartPhysician



# @receiver(post_save, sender=quickStartHospital)
# def saveTempGenericUser(sender,instance,created, **kwargs):
#     if created:
#         if instance.user is None:
#             generic_user = User.objects.get(username="unassigned")
#             generic_user.qs_hospitals = instance
#             generic_user.save()
#             instance.save()
#         print(quickStartHospital.objects.all())


# # @receiver(post_save, sender=quickStartPhysician)
# # def saveTempGenericUser(sender,instance,created, **kwargs):
# #     if created:
# #         if instance.user is None:
# #             generic_user = User.objects.get(username="unassigned")
# #             generic_user.hospitals.add(instance) 
# #             generic_user.save()
# #             instance.save()

