from django.urls import path
from support import views


app_name = 'support'

urlpatterns = [
    # path('downloadxls/tags/',views.downloadXLSStupidDuxkingfdumbfuckingbitch,name='downloadXLS2'),
    path('downloadxls/',view=views.downloadXLS,name='downloadXLS'),
    path('', view=views.contactUs, name='contactUs'),
    path('add/specialty/', views.addSpecialty,name='addSpecialty'),
    path('add/product/', views.addProduct, name='addProduct'),
    path('add/physician/',view=views.addPhysician,name='addPhysician'),
    path('add/hospital/',views.addHospital,name='addHospital'),
    # path('dumbbitch/',views.dumbbitch,name='dumbbitch')
  
   
]