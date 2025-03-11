from django.db import models
from django.contrib.auth.models import User

class BlacklistedAccessTokens(models.Model):
    '''
        Considering that SimpleJWT's blacklist app only blacklists the refresh tokens 
        and keeps the access ones valid, it is better to blacklist the access token.
        This will include a relation to the User table by using the user_id.
    '''

    blacklisted = models.CharField(max_length = 500)
    user = models.ForeignKey(User, related_name = 'token_user', on_delete = models.CASCADE)

