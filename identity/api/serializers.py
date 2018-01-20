from rest_framework import serializers
from django.contrib.auth.models import User
from datacenter.models import UserProfile

class UserLoginSerializer(serializers.Serializer):
    '''
    User Login Serializer
    '''
    username = serializers.CharField(min_length=1, max_length=255, required=True)
    password = serializers.CharField(min_length=1, max_length=255, required=True)