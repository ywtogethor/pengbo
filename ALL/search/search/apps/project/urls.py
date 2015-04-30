from django.conf.urls import patterns,url,include
from views import performance

urlpatterns = patterns('',
   url(r'delete/$',performance),
)
