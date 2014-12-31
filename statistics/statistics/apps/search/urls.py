#coding:UTF-8
from django.conf.urls import include,patterns,url
from views import homepage,search,search_stat

urlpatterns = patterns('',
  url(r'^$',homepage,name='homepage'),
  url(r'^search/$',search,name='search'),
  url(r'^search/(?P<date>\d{8})/$',search_stat,name='saerch_stat'),
)
