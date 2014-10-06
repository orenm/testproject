#!/usr/bin/env python
# Copyright (c) 2014 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

from django.http import HttpResponse

def home( request ):
    return HttpResponse( "This is my home page" )
