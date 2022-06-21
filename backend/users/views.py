from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework import generics, mixins

from .serializers import UserEditProfileSerializer, UserLoginSerializer, UserProfileSerializer, UserRegistrationSerializer, UserSerializer
from .renderers import UserRenderers
from .token import get_tokens_for_user
from .models import User

# Create your views here.

# UserRegistrationView
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

# UserLoginView
class UserLoginView(APIView):
     # Classes
    renderer_classes = [UserRenderers]

    # Post method to login user
    def post(self, request, format=None):
        # import pdb;pdb.set_trace()
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

# UserProfileView
class UserProfileView(APIView):
    
    # Classes
    renderer_classes = [UserRenderers]
    permission_classes = [permissions.IsAuthenticated]

    # Getting User Data
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response({'User Profile': serializer.data})


# Get List of Users, User Data, Edit User Profile
class UserListGetUpdateView(
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        generics.GenericAPIView
                        ):
     queryset = User.objects.all()
     permission_classes = [ permissions.IsAuthenticatedOrReadOnly ]

     def get(self, request, *args, **kwargs):
         pk = kwargs.get('pk')
        #  user = User.objects.filter(pk=pk)
        #  if pk is not None:
        #     return self.retrieve(request, *args, **kwargs)
         return self.list(request, *args, **kwargs)

     def put(self, request, *args, **kwargs):
        serializer = UserEditProfileSerializer(data=request.data, context={'user':request.user})
        # print(serializer.data)
        if serializer.is_valid(raise_exception=True):
            serializer2 = UserSerializer(request.user)
            message = f'Profile Edited successfully!\n {serializer2.data}'
            return Response({'message':message}, status=status.HTTP_200_OK)
        return Response({'Errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

     def get_serializer_class(self):
        if self.request.user.is_authenticated:
           return UserProfileSerializer
        return UserSerializer

# class UserChangePasswordView(APIView):
#     # Classes
#     renderer_classes = [UserRenderers]
#     permission_classes = [permissions.IsAuthenticated]

#     # Change user password
#     def post(self, request, format=None):
#         serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
#         if serializer.is_valid(raise_exception=True):
#             return Response({'message':'Password changed successfully!'}, status=status.HTTP_200_OK)
#         return Response({'Errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)