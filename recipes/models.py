from django.db import models
from .utils import unique_slug_generator
from django.db.models.signals import pre_save

from django.contrib.auth.models import User


import datetime
#get the current date and time




#a model class to represent the image table in the database with image url and a possibility for image file
class Image(models.Model):
    url = models.CharField(max_length=8000, blank=True, null=True)

    def __str__(self):
        return self.url

#a model class to represent the Vedio table 
class Vedio(models.Model):
    url = models.CharField(max_length=8000, blank=True, null=True)
    
    def __str__(self):
        return self.url

#a model class to represent the Ingredient table in the database with ingredients details
class Ingredient(models.Model):
    details = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.details


#a model class to represent the Instruction table in the database with Instruction details
class Instruction(models.Model):
    details = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.details


#a model class to represent the recipe table in the database with recipe name, many to many field to image ...etc
class Recipe(models.Model):
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    
    #relationship with profiles
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    #relationship with tables
    images = models.ManyToManyField(Image )
    ingredients = models.ManyToManyField(Ingredient )
    instructions = models.ManyToManyField(Instruction )
    vedios = models.ManyToManyField(Vedio)

    #fields
    name = models.CharField(max_length=1000, blank=True, null=True)
    rating = models.CharField(max_length=1000, blank=True, null=True , default="0 Ratings")
    time = models.CharField(max_length=1000, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True , null=True , blank=True)

    class Meta:
        #
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.name}--->{self.slug}"
    
    @property
    def image_urls(self):
        return [image.url for image in self.images.all() if "http" in image.url]

    @property
    def thumbnail(self):
        if self.images.all():
            return self.image_urls[0]
        else:
            return None
    
    @property
    def ingredients_details(self):
        return [ingredient.details for ingredient in self.ingredients.all()]
    
    @property
    def instructions_details(self):
        return [instruction.details for instruction in self.instructions.all()]
    
    @property
    def vedios_urls(self):
        return [vedio.url for vedio in self.vedios.all()]
    
    @property
    def to_dict(self):
        return {
            "thumbnail":self.thumbnail,
            "images": self.image_urls,
            "ingredients": self.ingredients_details,
            "instructions": self.instructions_details,
            "vedios": self.vedios_urls,

            "name": self.name,
            "slug": self.slug,
            "rating": self.rating,
            "time": self.time,

            "restaurant": self.user.username if self.user else "I-FOOD-TEAM",

            "created_at": self.created_at,
        }


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Recipe)