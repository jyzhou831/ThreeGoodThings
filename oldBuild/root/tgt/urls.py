from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^tgt/', include('tgt.foo.urls')),
    (r'^facebook/', include('django_facebook.urls')),
    (r'^accounts/', include('django_facebook.auth_urls')),
    (r'^accounts/', include('userena.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),


    (r'^api/saveGoodThing$','tgt.views.api_saveGoodThing'),
    (r'^api/delete','tgt.views.api_delete'),
    (r'^api/cheer','tgt.views.api_cheer'),
    (r'^api/uncheer','tgt.views.api_uncheer'),
    (r'^api/things','tgt.views.api_things'),
    (r'^api/saveSettings','tgt.views.api_saveSettings'),
    (r'^api/updateAuthToken','tgt.views.api_updateAuthToken'),

    (r'^user/([A-Za-z_0-9\.]*)/([0-9]+)$','tgt.views.gtview'),
    (r'^user/([A-Za-z_0-9\.]*)/$','tgt.views.index'),
    (r'^canvas/$', 'tgt.views.canvas'),
    (r'^privacy/$','tgt.views.privacy'),
    (r'^tos/$','tgt.views.tos'),
    (r'^favicon\.gif$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/favicon.gif'}),
    (r'^$', 'tgt.views.index'),
)
