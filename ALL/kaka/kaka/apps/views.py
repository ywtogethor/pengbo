from django.shortcuts import render
from django.http import HttpResponse
from django import template
# Create your views here.

def juxing(request):
    t=template.loader.get_template('ll.html')
    c=template.Context({'name':'cluo'})
    return HttpResponse(t.render(c))
