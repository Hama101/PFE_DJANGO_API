from django.db import models
from django.contrib.auth.models import User
#my model
from recipes.models import Recipe



#a profile class 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , unique=True)
    
    #image as a string
    avatar = models.CharField(max_length=8000 , null=True , blank=True )
    bg_image = models.CharField(max_length=8000 , null=True , blank=True )

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

