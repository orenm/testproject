#!/usr/bin/env python

from django import forms
from django.utils.translation import ugettext_lazy as _

class LoginForm( forms.Form ):
   username = forms.CharField(max_length=254) # self.fields[ 'username' ]
   password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
   error_messages = {}

   def __init__( self, request=None, *args, **kwargs):
      super( LoginForm, self ).__init__( *args, **kwargs )

#   username = forms.RegexField(
#      regex=r'^[\w.@+-]+$',max_length=30, label=_("Username"),
#      error_messages={'invalid': _("contain only letters, numbers @/./+/-/_")})
#   email = forms.EmailField( label=_("E-mail") )
#   password = forms.CharField( widget=forms.PasswordInput,
#                               label=_("Password") )
