from django.conf.urls import patterns,include,url
from views import two

urlpatterns = patterns("",

     url(r'^two/$',two),

   
)
