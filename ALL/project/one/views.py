#coding:UTF-8
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def def_one(request):
    return HttpResponse("大家好")
