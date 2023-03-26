from django import template
import json
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter()
def buildCSV(value):
    return ", ".join(list(map(lambda x: x.tag, list(value))))
