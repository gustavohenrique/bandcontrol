from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url':'/admin/'}),
    url(r'^admin/', include(admin.site.urls)),
)


from django.conf import settings
from django.views.generic.simple import direct_to_template
if settings.DEBUG:
    urlpatterns += patterns('',
         (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
         ('^404/$', direct_to_template, {'template': '404.html'}),
         ('^500/$', direct_to_template, {'template': '500.html'})
    )

