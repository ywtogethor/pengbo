#coding:UTF-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import main,link,aa,bb

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fenpuwang.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^fenpuwang/$',main),
    url(r'^link/$',link),
    url(r'^aa/$',aa),
    url(r'^bb/$',bb),
)
