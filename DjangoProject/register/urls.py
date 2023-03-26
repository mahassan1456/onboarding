from ast import *
from django.contrib import admin
from django.urls import include, path, re_path
from django.http import HttpResponse
# from polls.views import home
from django.conf import settings
from django.conf.urls.static import static


from register.views import *


app_name = 'register'

urlpatterns = [
    path('', register, name="register" ),
    path('register/manual/<int:id>/', registerManual, name="registerManual"),
    path('login/',login,name='login'),
    path('hospital/success/', accountConfirm, name="accountConfirm"),
    path('success/createcredentials/<int:id>/',createCredentials, name="createCredentials"),
    path('edit/hospital/<int:id>/', editHospital, name='editHospital'),
    path('edit/physician/<int:id>/', editPhysician, name='editPhysician'),
    path('edit/product/<int:id>/',editProduct,name='editProduct'),
    path('edit/specialty/<int:id>/',editSpecialty,name='editSpecialty'),
    path('logout/', logout, name="logout"),
     #  Delete Views
    path('remove/physician/<int:id>/',removePhysician1, name="removePhysician"),
    path('remove/physicianqs/<int:id>/',removePhysicianQs, name="removePhysicianQS"),
    path('remove/hospital/<int:id>/',removeHospital, name="removeHospital"),
    path('remove/qshospital/<int:id>/',removeQsHospital, name="removeQsHospital"),
    path('remove/product/<int:id>/',removeProduct, name="removeProduct"),
    path('remove/specialty/<int:id>/',removeSpecialty, name="removeSpecialty"),
    # ---------------------
    # End Delete Views
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 