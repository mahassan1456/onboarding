from django.urls import path
from ast import *
from django.contrib import admin
from django.http import HttpResponse
# from polls.views import home
from django.conf import settings
from django.conf.urls.static import static
from dashboard import views


app_name = 'dashboard'

urlpatterns = [

    path('master/main/', views.master_dashboard, name="master_dashboard"),
    path('staff/main/', views.dashboard, name="dashboard"),
    path('test/',views.test,name='f'),
    path('update/info/<int:id>/',view=views.updateInformationUser,name="updateInfo")
    
   
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 