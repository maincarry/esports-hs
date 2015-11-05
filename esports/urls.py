from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^$', 'hs.views.redirect_to_hs'),
                       url(r'^hs/', include('hs.urls', namespace="hs")),
                       url(r'^admin/', include(admin.site.urls)),
                       )
