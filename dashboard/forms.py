from django import forms
from djongo import models
from django.contrib.postgres.forms import JSONField

class ListFormField(forms.CharField):
    def to_python(self, value):
        if value is None:
            value = ""
        return value.split(",")

    def prepare_value(self, value):
        if value is None:
            value = []
        return ",".join(value)


class CustomListField(models.ListField):
    def formfield(self, **kwargs):
        return ListFormField(max_length=1000)



class CustomDictField(models.DictField):
    def formfield(self, **kwargs):
        return JSONField(required=False)

