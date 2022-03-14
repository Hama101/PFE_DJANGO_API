import string

import random 
from django.utils.text import slugify



def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def create_new_ref_number():
    return str(random.randint(10000, 99999))



def create_recipe_by_data(data , Recipe , user):
    recipe = Recipe(user = user)
    if data["name"] is not None:
        recipe.name = data["name"]
    if data['time'] is not None:
        recipe.time = data['time']
    if data['rating'] is not None:
        recipe.rating = data['rating']
    
    recipe.save()
    '''
        let's explain what is happening here:
        we are checking if data contains a key called ingredients,images,instructions and vedios
        if it does, we are going to save it to the database by looping through the list and creating a 
            new instance of the RecipeIngredients, RecipeImages, RecipeInstructions and RecipeVedios models
        than we update it with the new data
    '''
    if data["images"] is not None:
        for image in data['images']:
            recipe.images.create(url=image)
    if data["ingredients"] is not None :
        for ingredient in data['ingredients']:
            recipe.ingredients.create(details=ingredient)
    if data["instructions"] is not None:
        for instruction in data['instructions']:
            recipe.instructions.create(details=instruction)
    if data["vedios"] is not None:
        for vedio in data['vedios']:
            recipe.vedios.create(url=vedio)
    recipe.save()
    return recipe