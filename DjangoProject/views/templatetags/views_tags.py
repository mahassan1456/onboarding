from django import template
import json
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='countPhysicians')
@stringfilter
def countPhysicians(value,facility="0"):
    return value.countPhysicians(int(facility))



@register.filter(name='count')
@stringfilter
def count(value):
    return value.upper()