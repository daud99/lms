from django import template
import datetime
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

@register.filter
def get(value, arg):
    # getattr(value, arg)
    # print(type(value))
    # print(arg)
    # print(type(getattr(value, arg)))
    # return 1
    id = str(getattr(value, arg))
    print("id is ",id)
    print("type of id is ",type(id))
    return str(getattr(value, arg))

@register.filter
def parseUNIX(timestamp):
  date = datetime.date.fromtimestamp(timestamp)
  date = datetime.datetime.strftime(date, "%m/%d/%Y")
  return date