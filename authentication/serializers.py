from rest_framework import serializers
from django.contrib.auth.models import User

class AccountSerializer(serializers.ModelSerializer):
    '''
        Serializer used for account registration. It's using
        the built-in User model as the refrence and defines a new password_confirm
        field.
    '''

    password_confirm = serializers.CharField()
    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm']
    
    def validate(self, data):
        '''
            We write a custom validator which will
            check if the password_confirm value is equal to password.
        '''
        if not data['password'] == data['password_confirm']:
            raise serializers.ValidationError('Make sure to type the same password twice!')
        return data
