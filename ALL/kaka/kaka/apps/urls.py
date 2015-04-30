from django.conf.urls import include,patterns,url
from django.contrib import admin
#from views import juxing
urlpatterns=patterns("kaka.apps.views",
   url("cluo/$",'juxing'),

)
