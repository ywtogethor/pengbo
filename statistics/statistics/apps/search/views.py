#coding:UTF-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from models import SearchStat
import time
# Create your views here.


def homepage(request):
    return render_to_response("homepage.html")


def search(request):
    date = time.strftime("%Y%m%d",time.localtime())
    date=int(date)-1
    date=str(date)
    result=search_result(date)
    return render_to_response("search.html",{'select':result,'time':date})


def search_stat(request,date):
    result=search_result(date)
    return render_to_response("search_stat.html",{'select':result,'time':date})

def search_result(date):
    date = int(date)
    setList=SearchStat.objects.filter(date=date)
    deal_back=deal_data(setList)
    return  deal_back

def deal_data(data):
    total_list=[]
    for letter in data:
        dict_little={}
        new_list=str(letter).split('|')
        dict_little['keyword'] = new_list[0]
        dict_little['number'] = new_list[1]
        total_list.append(dict_little)
    return total_list

