from django.urls import path
from ast import *
from django.contrib import admin
from django.http import HttpResponse
# from polls.views import home
from django.conf import settings
from django.conf.urls.static import static
from views import views


app_name = 'views'

urlpatterns = [
    path('search/',views.searchViewHospital,name='searchView'),
    path('physician/', views.view_physicians, name="view_physicians"),
    path('logs/', views.view_activity, name="view_activity"),
    path('physician/qsview/', views.view_physicians_qs, name="view_physicians_qs"),
    path('qshospitals/', views.view_qs_hospitals, name="view_qs_hospitals"),
    path('get/qshospitals/', views.getQsHospitals, name="getQsHospitals"),
    path('filter/physician/listview/', views.fuckuyoustupidassdumbfuckingbitch, name='filterPhysiciansListView'),
    path('physician/staff/', views.view_physicians_staff, name="view_physicians_staff"),
    path('hospital/', views.view_hospitals, name="view_hospitals"),
    # Products View
    path('product/', views.view_products,name="view_products"),
    path('product/list/', views.viewProductList,name="viewProductList"),
    path('filter/hospital/',views.filterPhysicians,name='filterPhysicians'),
    path('filter/physician/',views.filterSpecialties, name='filterSpecialties'),
    path('build/productcards/', views.buildProductCards,name='buildProductCards'),
    path('toggle/view/',views.toggleAllorCurrent, name="toggleAllorCurrent"),
    # ---------------------
   
    path('specialty/', views.view_specialties, name="view_specialties"),
    path('recent_activity/', views.view_recent_activity, name="view_recent_activity"),
    path('invite_view/hospital/', views.invite_hospital_view, name='invite_hospital_view'),
    # path('invite_view/physician/', views.invite_physician_view, name='invite_physician_view'),
    path('filter/physicians/', views.filterPhysicians, name="filterPhysicians"),
    path('congrats/', views.congrats, name="congrats"),
    path('invite/reminder/<int:id>/', views.sendReminderHospital, name="sendReminder"),
    path('invite/reminder/physician/<int:id>/', views.sendReminderPhysician, name="sendReminderPhysician"),
    path('invite/reminder/manual/<int:id>/', views.sendReminderManual, name="sendReminderManual"),
    path('physician/detail/<int:id>/', views.physician_detail_view, name="physician_detail_view"),
    path('product/detail/<int:id>/', views.viewProductDetail, name="viewProductDetail"),
    path('product/detailpopup/', views.productDetailPopUp, name="productDetailPopUp"),
    
 
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

# /views/physician/detail/31/