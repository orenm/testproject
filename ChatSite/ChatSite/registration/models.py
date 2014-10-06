from django.db import models
from django.contrib.auth.models import User

class UserProfile( models.Model ):
   user = modles.OneToOneField( User )

   def __unicode__( self ):
      return self.user.username
