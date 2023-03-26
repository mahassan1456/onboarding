from django.urls import path

from medical import views


app_name = 'medical'

urlpatterns = [


    path('success/', view=views.success, name='success'),
    path('registernew/', views.reg, name='reg'),
    path('register/', views.register, name='register'),
    path('dashboard/', view=views.dashboard, name='dashboard'),
    path('createuser/<int:hospital_id>/', view=views.createuser, name='createuser'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('contactus/',views.contact_us, name='contactus'),
    path('facilities/', views.reviewAccount, name='reviewaccount'),
    path('details/<int:id>/', views.details, name='details'),
    path('confirmhospital/<int:id>/', views.confirmhospital, name='confirmhospital'),
    path('edithospital/<int:id>/', views.edit_hospital, name="edit_hospital"),
    path('fucku', views.fucku, name='fucku'),
    path('confirmapproval/', views.confirmApproval, name='confirmapproval'),
    path('removehospital/<int:id>/', views.removeHospital, name='removehospital'),
    path('approvetoken/verify/', views.approveJWT, name='approvejwt')
    
    
    
]