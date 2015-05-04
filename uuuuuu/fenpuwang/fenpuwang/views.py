#coding:UTF-8
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse
from django import template

def main(request):
    return render(request,"fenpuwang.html")

def link(request):
    return render(request,"link.html")

def aa(request):
    t = template.loader.get_template("bb/bb_bb.html")
    c = template.Context()
    response = HttpResponse(t.render(c))
    print response
    return response
    #response = HttpResponse("大家好")
    #print response
    #return response

def bb(request):
    response = render_to_response("bb/bb_bb.html")
    print response
    return response
