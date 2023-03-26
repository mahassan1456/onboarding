
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from .models import Specialty, ProductTags, Product,Physician



# from pproducts.models import ProductTags as pt, Product as p, Physician as pn, ImageTest as it, JsonProducts as jp, JsonProducts1 as jp1
# from django.forms.models import model_to_dict as mtd
# from django.contrib.auth.models import User
# from pproducts.serializers import PhysicianSerializer as sphys, JsonSerializer as js, JSONSerializerField as jsf, MySerializer as ms
class PhysicianSerializer(serializers.ModelSerializer):
    facility = serializers.SerializerMethodField()
    class Meta:
        model = Physician
        exclude = ['specialty_ph','productitems']

    def get_facility(self,obj):
        return obj.facility.name
        
class JsonSerializer(serializers.Serializer):
    products = serializers.JSONField(required=False)

class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""
    def to_internal_value(self, data):
        return data
    def to_representation(self, value):
        return value

# class MySerializer(serializers.ModelSerializer):
#     products = JSONSerializerField()
#     class Meta:
#         model = JsonProducts
#         fields = '__all__'

import json

# class JSONSerializerField(serializers.Field):
#     """ Serializer for JSONField -- required to make field writable"""

#     def to_internal_value(self, data):
#         json_data = {}
#         try:
#             json_data = json.loads(data)
#         except ValueError as e:
#             pass
#         finally:
#             return json_data
#     def to_representation(self, value):
#         return value



