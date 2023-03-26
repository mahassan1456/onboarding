from django.shortcuts import render
from pproducts.models import Specialty, ProductTags, Product,Physician
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.core import serializers
import json
from io import BytesIO as IO
import pandas as pd
from django.forms.models import model_to_dict
from django.contrib import messages
from django.urls import reverse
from medical.models import Hospital2
from pproducts.forms import AddProduct2Physician, AddProducts, AddProductTags,AddTags2PhysicianForm, AddHospitalAdmin, LinkedProductTags
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from mysite.settings import ADMIN_CONTACT
from django.contrib.auth.models import User
from pproducts.models import Physician
from medical.models import Hospital2 as Hospitals
# Create your views here.


def detail_physician(request,id):
    try:
        physician = Physician.objects.get(id=id)
    except (Physician.DoesNotExist,Exception) as error:
        return HttpResponse(content=f"{error}")
    return HttpResponse(content=f"Detailed Physician Page for {physician.get_full_name()} Coming Soon")

def detail_hospital(request,id):
    try:
        hospital = Hospitals.objects.get(id=id)
    except (Hospitals.DoesNotExist,Exception) as error:
        return HttpResponse(content=f"{error}")
    return HttpResponse(content=f"Detailed Hospital Page for {hospital.name} Coming Soon")

def detail_product(request):
    return HttpResponse(content="Detailed Product Page Coming Soon")

def detail_specialty(request):
    return HttpResponse(content="Detailed Specialty Page Coming Soon")
