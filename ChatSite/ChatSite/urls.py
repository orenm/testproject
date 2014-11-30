from django.conf.urls import patterns, include, url

from django.contrib import admin
import views

admin.autodiscover()

urlpatterns = patterns(
   '',
   # Examples:
   # url(r'^$', 'ChatSite.views.home', name='home'),
   # url(r'^blog/', include('blog.urls')),
   url( r'^admin/', include( admin.site.urls ) ),
   url( r'^$|^login$', views.login,
        { 'template_name': 'index.html' }, name='auth_login' ),
   url( r'^logout$', views.logout, {}, name='logout' ),
)
