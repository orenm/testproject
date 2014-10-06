#!/usr/bin/env python
# Copyright (c) 2014 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views

from registration.forms import LoginForm
import registration.views as views

urlpatterns = patterns( '', 
                        url(r'^$',
                            views.login, # callback when the url is hit.
                            # will create template context and call 
                            # create the template with TemplateResponse.
                            {'template_name': 'registration/login.html',
                             'extra_context': { 'next': 'main' }, 
                             },
                            name='auth_login'),
                        url(r'^main$',
                            views.main,
                            {},
                            name='main'),
                        )

