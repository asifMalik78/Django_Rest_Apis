from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer , UserSerializer as BaseUserSerializer
from rest_framework import serializers

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','username' , 'email' , 'first_name' , 'last_name' , 'password']


class UserSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','username' , 'email' , 'first_name' , 'last_name']