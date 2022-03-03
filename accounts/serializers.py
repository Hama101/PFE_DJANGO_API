from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


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

        return user




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


# class ProfilSerializer(serializers.ModelSerializer):
#     class Meta :
#         model = Profil
#         fields = '__all__'

#     def	save(self):
#         user = self.validated_data['user']
#         if not user:
#             raise serializers.ValidationError({'user': 'user must match.'})
#         profil = Profil(
#             user = user ,
#             is_chef = self.validated_data['is_chef']
#         )
#         profil.save()
#         return profil

# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = '__all__'

#     def	save(self):
#         user = self.validated_data['user']
#         if not user:
#             raise serializers.ValidationError({'user': 'user must match.'})
#         if not user.profil.is_chef:
#             raise serializers.ValidationError({'user': 'user must be a cheff to add post.'})
#         post = Post(
#         user = user ,
#         title = self.validated_data['title'],
#         description = self.validated_data['description'],
#         #img = self.validated_data['img'],
#         price = self.validated_data['price'],
#         )
#         post.save()
#         return post

#     def update(self , instance , validated_data):
#         user = User.objects.get(id = validated_data.get('user', instance.user))
#         instance.user = user
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.price = validated_data.get('price', instance.price)
#         instance.save()
#         return instance