from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Profile

from recipes.serializers import ImageSerializer
#User serializers
class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ["email" , "username" , "password" , "password2"]
        extra_kwargs = {
				'password': {'write_only': True},
		}

    def	save(self):
        user = User(
                    email=self.validated_data['email'],
                    username=self.validated_data['username']
                )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)        
        user.save()
        #creating profile with null values and assgin it for the user when ever we create the user
        profile = Profile(user=user)
        profile.save()

        return user



#login serializers
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


#profile serializers
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar', 'bg_image']