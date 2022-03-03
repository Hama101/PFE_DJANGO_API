from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *

from knox.models import AuthToken
from django.contrib.auth import login
#rest framework
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, permissions


#classes for login api auth 

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    
    
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


    def get_post_response_data(self, request, token, instance):
        UserSerializer = self.get_user_serializer_class()

        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        if UserSerializer is not None:
            data["user"] = UserSerializer(
                request.user,
                context=self.get_context()
            ).data
        return data


#this class hundels the user permissions and permissions for the api
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
    permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

#this view function hundel the user singup process
@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['id']= user.id
            data['email'] = user.email
            data['username'] = user.username
        else:
            data = serializer.errors
            return Response(data)

        user = User.objects.get(username=data['username'])
        data["token"] = AuthToken.objects.create(user)[1]
        return Response(data)


# @api_view(['POST'])
# def addprofil(request):
#     if request.method == 'POST':
#         serializer = ProfilSerializer(data=request.data)
#         data = {}
#         print("validating")
#         if serializer.is_valid():
#             print("validated")
#             profil = serializer.save()
#             data['response'] = 'successfully registered new profil.'
#             print(profil.user)
#             data['user'] = profil.user.username
#             data['is_chef'] = profil.is_chef
#         else:
#             data = serializer.errors
#         return Response(data)


