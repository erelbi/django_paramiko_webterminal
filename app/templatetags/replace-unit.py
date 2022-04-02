from django import template
from django.template import Template

register = template.Library()

@register.filter
def replace(value):
    return value.replace("}","-")