from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import def_one
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^get/$',def_one,name='get'),
)

