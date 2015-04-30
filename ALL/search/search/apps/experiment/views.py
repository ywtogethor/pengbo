from django.shortcuts import render
from django import template
from django.http import HttpResponse

# Create your views here.
def deal(request):
    t=template.Template('I am {{ happy }}')
    c=template.Context({'happy':'happy'}) 
    return HttpResponse(t.render(c))   
