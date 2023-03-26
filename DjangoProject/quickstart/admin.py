from django.contrib import admin

from quickstart.models import quickStartHospital1 as quickStartHospital, quickStartPhysician






admin.site.register([quickStartHospital,quickStartPhysician])

