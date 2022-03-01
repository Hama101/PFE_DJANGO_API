from django.db import models
from .utils import unique_slug_generator
from django.db.models.signals import pre_save

#a model class to represent the image table in the database with image url and a possibility for image file
class Image(models.Model):
    url = models.CharField(max_length=8000, blank=True, null=True)
    # image_file = models.ImageField(upload_to='images/', blank=True, null=True)

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
    #relationship with tables
    images = models.ManyToManyField(Image , null=True, blank=True)
    ingredients = models.ManyToManyField(Ingredient , null=True, blank=True)
    instructions = models.ManyToManyField(Instruction , null=True, blank=True)
    vedios = models.ManyToManyField(Vedio, null=True, blank=True)
    #fields
    name = models.CharField(max_length=1000, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return f"{self.name}--->{self.slug}"
    
    @property
    def thumbnail(self):
        if self.images.all():
            return self.images.all()[0].url
        else:
            return None

    @property
    def image_urls(self):
        return [image.url for image in self.images.all()]
    
    @property
    def ingredients_details(self):
        return [ingredient.details for ingredient in self.ingredients.all()]
    
    @property
    def instructions_details(self):
        return [instruction.details for instruction in self.instructions.all()]
    
    @property
    def vedios_urls(self):
        return [vedio.url for vedio in self.vedios.all()]

    def to_dict(self):
        return {
            "images": self.image_urls,
            "ingredients": self.ingredients_details,
            "instructions": self.instructions_details,
            "vedios": self.vedios_urls,

            "name": self.name,
            "slug": self.slug,
            "rating": self.rating,
            "time": self.time,
        }


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Recipe)