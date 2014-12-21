#!/usr/bin/env python
# Copyright (c) 2014 Arista Networks, Inc.  All rights reserved.

from django.template.response import TemplateResponse
from django.contrib.sites.models import get_current_site
from django.shortcuts import resolve_url
from django.http import HttpResponseRedirect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import is_safe_url
from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    if request.user.is_authenticated():
       return TemplateResponse(request, template_name, RequestContext(request),
                               current_app=current_app)
    else:
       if request.method == "POST":
           form = authentication_form(request, data=request.POST)
           if form.is_valid():
               auth_login(request, form.get_user())
               return TemplateResponse(request, template_name, RequestContext(request),
                                       current_app=current_app)
       else:
           form = authentication_form(request)

       current_site = get_current_site(request)

       context = {
           'form': form,
           redirect_field_name: '',#redirect_to,
           'site': current_site,
           'site_name': current_site.name,
       }
       if extra_context is not None:
           context.update(extra_context)
       
       return TemplateResponse(request, template_name, context,
                               current_app=current_app)

def logout( request ):
   auth_logout( request )
   return HttpResponseRedirect( 'login' )

import ImageStreamer
import base64
from django.http import HttpResponse

def textImage( request ):
   image = "nothing"
   if not ImageStreamer.stream.isConnected:
      try:
         ImageStreamer.stream.connect()
      except:
         HttpResponse( "Camera not ready" )
   try:
      image = base64.b64encode( ImageStreamer.stream.getNextImage() )
   except EOFError:
      pass
   return HttpResponse( image )
   

def test( request ):
   return TemplateResponse( request, 'test.html' )
   image = 'nothing'
   try:
      if not ImageStreamer.stream.isConnected:
         ImageStreamer.stream.connect()
      image = base64.b64encode( ImageStreamer.stream.getNextImage() )
      print image[0:100]
   except:
      image = 'nothing'
      pass
   return TemplateResponse(request, 'test.html',  { 'image_string' : image }, None )
