from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import *


@api_view(['POST'])
def registration_view(request):
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    User.objects.create_user(**serializer.validated_data)
    return Response(status=status.HTTP_201_CREATED, data={
        "message" : "User create successfuly!"
    })

@api_view(['POST'])
def authentication_view(request):
    serializer = ValidateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(**serializer.validated_data)
    if not user:
        return Response(status=status.HTTP_401_UNAUTHORIZED,
                        data= {'message' : "Username or pass are wrong!"})
    token, created = Token.objects.get_or_create(user=user)
    return Response(data={"key" : token.key})

