from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import hello,world,love,module,fast,happy,one,please,get,idfunction,dictionary
urlpatterns = patterns('kaka.views',
    # Examples:
    # url(r'^$', 'kaka.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$',hello),
    url(r'^world/$',world),
    url(r'^love/$',love),
    url(r'^module/$',module),
    url(r'^fast/$',fast),
    url(r'^happy/$',happy),
    url(r'^one/$',one),
    url(r'^please/$',please),
    url(r'^get/$',get),
    url(r'^id/$',idfunction),
    url(r'^test/$','test'),
    url(r'^happy_happy/','happy_happy')
)
urlpatterns += patterns('kaka.views',
    url(r'^football/$','football',{'template_name':'football.html'}), 
    url(r'^score/(?P<score_id>\d+)/$','score'),
    url(r'^three/$','three'),
    url(r'^common_one/$','common_one'),
    url(r'^common_two/$','common_two'),
    url(r'^kaka/',include('kaka.apps.urls'))
)

urlpatterns += patterns('',
 url(r'^dictionary/$',dictionary),
)
