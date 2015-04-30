#coding:UTF-8
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse

def main(request):
    return render(request,"fenpuwang.html")

def link(request):
    return render(request,"link.html")

def aa(request):
    return HttpResponse("大家好")

def bb(request):
    return render_to_response("bb.html")
