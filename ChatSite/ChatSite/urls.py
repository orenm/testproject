from django.conf.urls import patterns, include, url

from django.contrib import admin
import ChatSite.registration.urls
import ChatSite.registration.auth_urls
admin.autodiscover()

urlpatterns = patterns(
   '',
   # Examples:
   # url(r'^$', 'ChatSite.views.home', name='home'),
   # url(r'^blog/', include('blog.urls')),
   url( r'^admin/', include( admin.site.urls ) ),
   url( r'^converse1/', include( ChatSite.registration.urls ) ),
   #url( r'^converse1/$', 'ChatSite.views.home', name='home' ),
)
