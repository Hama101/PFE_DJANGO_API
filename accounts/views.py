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
from rest_framework.decorators import api_view , permission_classes 
from rest_framework import generics, permissions
from rest_framework.views import APIView
#my utils imports
from .EmailSender import Emailer


HOST = "http://localhost:8000"
FRONTEND_HOST = "http://localhost:3000"



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
            #send mail here
        else:
            data = serializer.errors
            return Response(data)

        user = User.objects.get(username=data['username'])
        data["token"] = AuthToken.objects.create(user)[1]
        return Response(data)

'''
    the above section is the old version of our api that we will delete soon !
'''



#get profile by username
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def profiles_list(request):
    profiles = Profile.objects.all()
    if profiles.count():
        return Response([profile.to_dict for profile in profiles])



#get profile by username
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def profile(request, username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        data = profile.to_dict
        return Response(data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'User not found'})
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND , data={"error": "Profile not found"})


#update the profile of the user
@swagger_auto_schema(method='put', request_body=ProfileSerializer)
@api_view(['PUT'])
def update_profile(request):
    print(request.user)
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        #create a new profile
        profile = Profile(user=request.user)
        profile.save()

    if request.method == 'PUT':
            serializer = ProfileSerializer(instance=profile , data=request.data)
            data = {}
            if serializer.is_valid():
                serializer.save()
                data['response'] = 'successfully updated profile.'
                data['profile'] = serializer.data
            else:
                data = serializer.errors
                return Response(data)
            return Response(data)



#jwt auth not knox
class RegisterView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        try:
            data = request.data

            first_name = data['first_name']
            last_name = data['last_name']
            username = data['username']
            email = data['email']
            password = data['password']
            re_password = data['re_password']

            if password == re_password:
                if len(password) >= 8:
                    if not User.objects.filter(username=username).exists():
                        user = User.objects.create_user(
                            first_name=first_name,
                            last_name=last_name,
                            username=username,
                            email=email,
                            password=password,
                        )
                        
                        user.save()
                        #create a new null profile
                        profile = Profile.objects.create(user=user)
                        profile.save()
                        
                        #send mail
                        data_mail = {
                            "email_subject": "Welcome to IFOOD where you can find the best food in the world !",
                            "email_body": f"Thank you for signing up to IFOOD, we hope you enjoy your time here !\n\n to verify your email address, please click on the link below:\n\n {HOST}/accounts/set-profile-verified/{user.username}\n\n Best regards,\n\n IFOOD team",
                            "to_email": email,
                        }
                        Emailer.send_email(data_mail)

                        if User.objects.filter(username=username).exists():
                            return Response({
                                'success': 'Account created successfully',
                                'user': UserSerializer(user).data,
                                'profile': ProfileSerializer(profile).data,
                                },
                                status=status.HTTP_201_CREATED
                            )
                        else:
                            return Response(
                                {'error': 'Something went wrong when trying to create account'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )
                    else:
                        return Response(
                            {'error': 'Username already exists!'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {'error': 'Password must be at least 8 characters in length'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'error': 'Passwords do not match'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            print(e)
            return Response(
                {'error': 'Something went wrong when trying to register account'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoadUserView(APIView):
    def get(self, request, format=None):
        try:
            user = User.objects.get(username=request.user.username)
            #load the user profile
            profile = Profile.objects.get(user=user)
            user = UserSerializer(user)
            return Response(
                {
                    'user': user.data,
                    'profile': profile.to_dict,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(
                {'error': 'Something went wrong when trying to load user'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


#get profile by username
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def set_profile_verified(request , username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        profile.verified = True
        profile.save()
        return redirect('http://localhost:3000')
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'User not found'})
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND , data={"error": "Profile not found"})