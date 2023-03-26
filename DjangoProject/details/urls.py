from django.urls import path
from ast import *
from django.contrib import admin
from django.http import HttpResponse
# from polls.views import home
from django.conf import settings
from django.conf.urls.static import static
from details import views


app_name = 'details'

urlpatterns = [

    path('physician/<int:id>/', views.detail_physician, name="detail_physician"),
    path('hospital/<int:id>/', views.detail_hospital, name="detail_hospital"),
    path('product/', views.detail_product,name="detail_product"),
    path('specialty/', views.detail_specialty, name="detail_specialty")
    
   
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 