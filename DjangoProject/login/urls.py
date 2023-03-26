"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from ast import *
from django.contrib import admin
from django.urls import include, path, re_path
from django.http import HttpResponse
# from polls.views import home
from django.conf import settings
from django.conf.urls.static import static
from mysite import views

from login.views import *


app_name = 'login'

urlpatterns = [
    path('', loginUser, name="login" ),
    path('setprofile/', createProfile, name='createProfile' ),
    path('forgotpassword/', forgot_password, name='forgot_password'),
    path('newpassword/', reset_password, name='reset_password'),
    path('viewadmins/',view=admins,name='admins'),
    path('removeadmin/<int:id>/',removeAdmin, name='removeadmin'),
    path('editadmin/<int:id>/', editAdmin, name='editadmin'),
    path('register/', register1, name='register'),
    path('approval/admin/', approveHospitalFromLink,name='approveFromEmail'),
    # re_path(r'^.*$', loginUser, name="logincatchall"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
