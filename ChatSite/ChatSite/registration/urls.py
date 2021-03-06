from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.conf import settings

from registration.forms import LoginForm
import registration.views as views

urlpatterns = patterns( '', 
                        url(r'^$|^login$',
                            views.login, # callback when the url is hit.
                            # will create template context and call 
                            # create the template with TemplateResponse.
                            {'template_name': 'registration/index.html',
                             'extra_context': { 'next': 'index' }, 
                             },
                            name='auth_login'),
                        url(r'^logout$',
                            views.logout,
                            {},
                            name='logout'),
                        )
# this will add a search to app/static files such as images
# will not work in production
if settings.DEBUG:
   urlpatterns += [ 
      url( r'^(?P<path>.*)$', 'django.views.static.serve', 
          { 'document_root' : settings.PROJECT_PATH + '/registration'}) ]

