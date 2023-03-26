from django import template
import json
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='countPhysicians')
def countPhysicians(value,facility=0):
    return value.countPhysicians(facility)

@register.filter(name='string2json')
def string2json(value):
    if type(value) == str:
        return json.loads(value)['name']
    else:
        return value['name']

@register.filter(name='test')
def test(value):
    return value

@register.filter(name='convert')
def convert(value):
    return len(value)

@register.filter(name='toJ')
def toJ(value):
    return json.dumps(value)

@register.filter(name="getItem")
def get_item(dictionary, key):
    # print(type(dictionary))
    # print(type(json.loads(dictionary)))
    # if isinstance(dictionary, str):
    #     return json.loads(dictionary).get(key,'FuckYouDjango')
    return dictionary.get(key,"fuckudjango")

@register.filter
def get_type(value):
    return type(value)
    
@register.filter
def toString(value):
    return str(value)

@register.filter
def toInt(value):
    return int(value)

@register.filter
@stringfilter
def short_desc(value):
    return value[0:200]
