from django import template
from django.template import Template

register = template.Library()

@register.filter()
def to_int(value):
    return int(value)