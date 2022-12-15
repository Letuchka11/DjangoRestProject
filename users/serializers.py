from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers

class ValidateUserSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=2,max_length=15)
    password = serializers.CharField(min_length=6)



class CreateUserSerializer(ValidateUserSerializer):
    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except:
            return username
        raise ValidationError("This username already exists!")

