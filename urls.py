from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^bandcontrol/', include('bandcontrol.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^$', 'django.views.generic.simple.redirect_to', {'url':'/admin/'}),
    (r'^admin/', include(admin.site.urls)),
)

from django.conf import settings
if settings.DEBUG == True:
    urlpatterns += patterns('',
        (r'^media/(.*)','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    )
