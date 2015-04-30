from django.conf.urls import patterns,include,url
from views import deal
urlpatterns = patterns('',
    url(r'select/$',deal), 

)
