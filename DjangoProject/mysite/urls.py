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




urlpatterns = [
    path('', views.home, name='home'),
    path('nefariousdb/', admin.site.urls),
    path('medical/', include('medical.urls')),
    path('pproducts/', include('pproducts.urls')),
    path('login/', include('login.urls')),
    path('quickstart/',include('quickstart.urls')),
    path('register/', include('register.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('details/', include('details.urls')),
    path('views/', include('views.urls')),
    path('support/', include('support.urls')),
    # path('editor/', include('django_summernote.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += re_path(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#             'document_root': settings.MEDIA_ROOT,
#         })
