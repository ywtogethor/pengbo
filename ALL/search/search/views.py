from django.http import HttpResponse
from django import template
from django.shortcuts import render

def one(request):
    t=template.Template("today is a sunshine {{ how }}")
    c=template.Context({'how':'weather'})
    return HttpResponse(t.render(c))
