from django.shortcuts import render
from django import template
from django.http import HttpResponse
# Create your views here.


def performance(request):
    t=template.Template('His performance is very {{ adj }}') 
    c=template.Context({'adj':'wonderful'})
    return HttpResponse(t.render(c))
