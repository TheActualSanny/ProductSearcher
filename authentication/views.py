from rest_framework.views import APIView
from .serializers import AccountSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import BlacklistedAccessTokens
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed, ValidationError

class LoginEndpoint(APIView):
    '''
        Class which is used to log the user in.
        For the API, JWT Authentication is used.
    '''
    permission_classes = [AllowAny]
    def post(self, request):
        username, password = request.data.get('username'), request.data.get('password')
        possible_acc = authenticate(username = username, password = password)
        if not possible_acc:
            raise ValidationError('Make sure to input correct credentials!')
        refresh_token = RefreshToken.for_user(possible_acc)
        return Response({'message' : 'User authenticated! use the access token for API access',
                         'access_token' : str(refresh_token.access_token),
                         'refresh_token' : str(refresh_token)})


class RegisterEndpoint(APIView):
    '''
        Registers the user and generates a new JWT Token.
    '''
    permission_classes = [AllowAny]
    def post(self, request):
        creds = AccountSerializer(data = request.data)
        if creds.is_valid():
            new_user = User.objects.create_user(username = creds.data.get('username'),
                                                password = creds.data.get('password'))
            new_token  = RefreshToken.for_user(user = new_user)
            
        else:
            raise AuthenticationFailed('Please, input the correct password in both fields!')
        return Response({'message' : 'Account created! Use the returned access token for API access',
                         'access_token' : str(new_token.access_token),
                         'refresh_token' : str(new_token)})
    
    def get(self, request):
        return Response({'message' : 'Welcome! Please register an account.'})
    
class LogoutEndpoint(APIView):
    '''
        As we are using JWT tokens, this will simply
        blacklist them.
    '''
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message' : 'Pass the JWT token which you wish to blacklist.'})

    def post(self, request):
        token_passed = request.META.get('HTTP_AUTHORIZATION', ' ').split(' ')[1]
        BlacklistedAccessTokens.objects.create(blacklisted = token_passed,
                                               user = request.user)
        return Response({'message' : 'Successfully logged out, access token now blacklisted.'})