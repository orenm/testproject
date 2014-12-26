from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic import TemplateView
from django.template.response import TemplateResponse
import views

admin.autodiscover()


def DirectToTemplate( request ):
   print "HA"
   return TemplateResponse( request, 'vid.html' )

urlpatterns = patterns(
   '',
   # Examples:
   # url(r'^$', 'ChatSite.views.home', name='home'),
   # url(r'^blog/', include('blog.urls')),
   url( r'^admin/', include( admin.site.urls ) ),
   url( r'^$|^login$', views.login,
        { 'template_name': 'index.html' }, name='auth_login' ),
   url( r'^logout$', views.logout, {}, name='logout' ),
   url( r'^test$', views.test, {} ,name='test' ),
   url( r'^textImage$', views.textImage, {} ,name='textImage' ),
   url( r'^video$', DirectToTemplate, {}, name='' ),
)
