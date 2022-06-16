from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

from .serializers import UserLoginSerializer, UserRegistrationSerializer
from .renderers import UserRenderers
from .token import get_tokens_for_user

# Create your views here.

# Registration
class UserRegistrationView(APIView):
    # Classes
    renderer_classes = [UserRenderers]

    # Post method to create user
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'message': 'Congratulations! Registration Successful.'}, status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        return Response({'Errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Login
class UserLoginView(APIView):
     # Classes
    renderer_classes = [UserRenderers]

    # Post method to login user
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'message':'Login Successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'Errors':{'non_field_errors':['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)