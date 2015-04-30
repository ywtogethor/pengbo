from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import one 
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'search.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^database/',include('search.apps.experiment.urls')),
    url(r'^$',one),
    url(r'^data/',include('search.apps.project.urls'))
)
