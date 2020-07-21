from django import template
import json

register = template.Library()

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.filter
def parsejson(arg1, arg2):
    return json.loads(arg1)