from django.db import models
from django.contrib.auth.models import User
#my model
from recipes.models import Recipe



#a profile class 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , unique=True)
    
    #verified = models.BooleanField(default=True)#setting default as true just for test purposes

    #image as a string
    avatar = models.CharField(max_length=8000 , null=True , blank=True , default="https://e7.pngegg.com/pngimages/799/987/png-clipart-computer-icons-avatar-icon-design-avatar-heroes-computer-wallpaper.png" )
    bg_image = models.CharField(max_length=8000 , null=True , blank=True , default="https://webgrowhub.com/wp-content/uploads/2020/12/photo-1552566626-52f8b828add9.jpg")


    #recipes the recipes will be linked by the forgien key to the profile
    @property
    def get_recipes(self):
        return Recipe.objects.filter(user = self.user)

    def __str__(self):
        return self.user.username
    
    @property
    def name(self):
        return self.user.username
    
    @property
    def to_dict(self):
        return {
            'name': self.user.username,
            'avatar': self.avatar ,
            'bg_image': self.bg_image ,
            "Recipes": [recipe.to_dict for recipe in self.get_recipes]
        }

