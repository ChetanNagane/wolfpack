from dataclasses import field, fields
from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields= ['id','email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def save(self, **kwargs):
        super().save(**kwargs)
        user = User.objects.get(email=self.validated_data['email'])
        password = self.validated_data['password']
        if password is not None:
            user.set_password(password)
            user.save()
        return user