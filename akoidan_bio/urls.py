from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'akoidan_bio.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'request', 'akoidan_bio.views.requests'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^form/', 'akoidan_bio.views.change_form'),
    url(r'^register', 'akoidan_bio.views.register'),
)
