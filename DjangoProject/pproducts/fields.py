from django.db import models
import json
from datetime import datetime

class MyJsonField(models.JSONField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def from_db_value(self, value, expression, connection):
       
        if value is None:
            return None
        if isinstance(value,str):
            return json.loads(value)
        if isinstance(value,dict):
            return value

    def to_python(self, value):
        print("testtttt where this fucking goes t python")
        if isinstance(value,str):
            return json.loads(value)
        if value is None:
            return value
        if isinstance(value,dict):
            return value
        # return super().to_python(value)

    def TagQuerySetToDict(self,productTag):
        values = list(productTag.products.all().values())
        d = {'Back': [{'prod1': 'back brace', 'prod2': 'neck brace'}],'Chest': [{'prod1': 'cast', 'prod2': 'defibrialtor'}]}
        for product in values:
            product['created_at'] = str(product['created_at']) if product['created_at'] is not None else None
            product['updated_at'] = str(product['updated_at']) if product['updated_at'] is not None else None

        return values

    def get_db_prep_value(self, value ,connection ,prepared=False):
    
        from pproducts.models import ProductTags

        if isinstance(value,dict):
            value = json.dumps(value)
            return value
        if isinstance(value, str):
            return value
        
        return super().get_db_prep_value(value, connection, prepared=True)
    