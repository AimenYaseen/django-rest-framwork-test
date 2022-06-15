from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserRegistrationSerializer

# Create your views here.
class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg': 'This is a post request for Registration'}, status=status.HTTP_201_CREATED)
        return Response({'Errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        