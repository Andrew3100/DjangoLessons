from .models import *
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea
from django.http import HttpRequest
from django.shortcuts import render
from django import forms
from .models import *
from .forms import Form

section = Sections.objects.filter(id=request.GET['section'])

class Form(ModelForm):
    class Meta:
        model = TableOch
        fields = ['country','higher_education','mean_education','graduate_students','first_course','excepted']

