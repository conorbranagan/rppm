from django.conf.urls.defaults import *
from radioparadise.playlists.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^radioparadise/', include('radioparadise.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/path/to/webapps/radioparadise/radioparadise/playlists/static', 'show_indexes': False}),
	(r'^cron/scrape/', scrape),
	(r'^$', index),
	(r'^list/(?P<start>[0-9]+)/(?P<end>[1-9][0-9]*)$', listing),
	(r'^save/$', save),
	(r'^playlist/(?P<uid>[A-Za-z0-9]+)/$', saved),
)
