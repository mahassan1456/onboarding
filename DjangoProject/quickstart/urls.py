from django.urls import path

from ast import *
from django.contrib import admin
from django.urls import include, path, re_path
from django.http import HttpResponse
# from polls.views import home
from django.conf import settings
from django.conf.urls.static import static
from mysite import views
from quickstart import views


app_name = 'quickstart'

urlpatterns = [
    path('physician/', views.quickStartPhysician, name="quickStartPhysician" ),
    path('staff/physician/', views.quickStartPhysicianStaff,name='qs_staff'),
    path('token/validate/', views.validateToken,name='validateToken'),
    path('hospital/', views.quickStartHosital,name="quickStartHospital"),
    path('invited/hospital/<int:id>/', views.invitedHospital, name="invitedHospital"),
    path('welcome/physician/<int:id>/', views.invitedPhysician, name='invitedPhysician'),
    path('build/products/',views.buildProducts,name="buildProducts"),
    path('assignadmin/<int:id>/',views.assignAdmin, name="assignAdmin"),
    path('thankyou/physician/<int:id>/',views.thinkYou, name="thank_you")
    
   
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 