from django.conf.urls.defaults import *

urlpatterns = patterns('',
   (r'^$', 'defacement.apps.views.index'),
   (r'^admin/', include('django.contrib.admin.urls')),
   (r'^(\d{1,})/$', 'defacement.apps.views.website'),
   (r'^defacer/$', 'defacement.apps.views.defacer'),
   (r'^defacer/(\d{1,})/$' , 'defacement.apps.views.defacer_filter'),
   (r'^whois/([^/]+)/$', 'defacement.apps.views.whois'),
   (r'^search/$', 'defacement.apps.views.search'),
   (r'^whois/$', 'defacement.apps.views.whois_all'),
   (r'^detail/([^/]+)/$', 'defacement.apps.views.date_detail'),
   (r'^([^/]+)/([^/]+)/$', 'defacement.apps.views.filter'),
   (r'^detail/$', 'defacement.apps.views.detail'),
)


