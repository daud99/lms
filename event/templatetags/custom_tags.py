from django import template
import json
from LMS import common

register = template.Library()

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.filter
def parsejson(arg1, arg2):
    return json.loads(arg1)

@register.filter
def parseLogLat(value, arg):
    return common.getLocationFromLangLat(value)

@register.filter
def addWithComma(value, arg):
    l =common.getLangLat(value)
    return arg+l