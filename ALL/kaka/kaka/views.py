from django.shortcuts import render_to_response,render
from django.http import HttpResponse
from django import template
def world(request):
    t=template.loader.get_template("world.html")
    c=template.Context({'a':'1'})
    return HttpResponse(t.render(c))

def hello(request):
    aa="hello world"
    return HttpResponse(aa)

def love(request):
    t=template.loader.get_template("love.html")
    c=template.Context({
       'a':'11111',
       'b':'22222',
       'c':'33333',
       'd':'44444'
    })
    return HttpResponse(t.render(c))

def module(request):
    t=template.Template('my name is {{ name }}')
    c=template.Context({'name':'yupengbo'})
    return HttpResponse(t.render(c))

def fast(request):
    return render_to_response("fast.html",{'a':'hope cici happy'})

def happy(request):
    return render_to_response("template/happy.html")

def one(request):
    return render_to_response("demo_one.html")

def please(request):
    a=request.path
    b=request.get_host()
    c=request.get_full_path()
    d=request.is_secure()
   # a_a=request.META['HTTP_REFERRER']
    a_b=request.META['HTTP_USER_AGENT']
    a_c=request.META['REMOTE_ADDR']
    return HttpResponse(a_c)

def get(request):
    t=template.loader.get_template("form.html")
    c=template.Context({"a":"123"})
    return HttpResponse(t.render(c))

def idfunction(request):
    if 'na' in request.GET:
        message='my name is '+request.GET['na']
    else:
        message='your submitted an empty form.'
    return render_to_response("id.html",{'a':message})

def test(request):
    t=template.Template("I like {{ name }}")
    c=template.Context({'name':'wangruijing'})
    return HttpResponse(t.render(c))

def happy_happy(request):
    t=template.Template("I am very {{ adj }}")
    c=template.Context({'adj':'happy'})
    return HttpResponse(t.render(c))

def football(request,template_name):
    return render(request,template_name)

def score(request,score_id):
    t=template.Template('I hope I can {{ score }}')
    c=template.Context({ 'score':score_id})
    return HttpResponse(t.render(c))

def three(request):
    t=template.loader.select_template(['three.html'])
    c=template.Context({'a':'123'})
    return HttpResponse(t.render(c))

def common(request):
    return {
       'a':'mother',
       'b':'father',
       'c':'brother'
} 

def common_one(request):
    t=template.loader.get_template("common_one.html")
    c=template.RequestContext(request,{'d':'wangruijing'},processors=[common])
    return HttpResponse(t.render(c))
def common_two(request):
    #t=template.loader.get_template("common_two.html")
    #c=template.RequestContext(request,{'d':'zhangsisi'},processors=[common])
    return render_to_response("common_two.html",{'d':'zhangsisi'},
        context_instance=template.RequestContext(request,processors=[common])
)
def dictionary(request):
    dic ={'c':'cluo','k':'kaka','m':'messi'}
    #dic = ['cluo','kaka','messi']
    #dic = [('c','cluo'),('k','kaka'),('m','messi')]
    #dic = {'football':[{'c':'cluo','k':'kaka','m':'messi'}]}
    return render(request,'dictionary.html',{'total':dic})
