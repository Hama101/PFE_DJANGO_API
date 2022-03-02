#django stuff
from django.shortcuts import render , redirect
from django.http import JsonResponse
from .models import Recipe
from django.core.paginator import Paginator
#rest framework
from .serializers import RecipeSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
#my utils
from .utils import create_recipe_by_data


#usefull and global functions
#this function is used to paginate some data
def paginated_data(data,page_number=None,page_size=10):
    if not page_number:
        page_number = 1
    paginator = Paginator(data, page_size)
    page_objs = paginator.get_page(page_number)
    return page_objs


# Create your views here.
def index(request):
    return redirect('recipes:recipe_list')


#a get method to get all the list of recipes
#endpoint="http://127.0.0.1:8000/recipes/recipes-list/"
@api_view(['GET'])
def recipe_list(request):
    recipes = Recipe.objects.all()
    page_number = request.GET.get('page')
    #set a default page number if not specified
    recipes = paginated_data(recipes, page_number,20)
    return JsonResponse({"data": [recipe.to_dict() for recipe in recipes]},json_dumps_params={'indent': 4})


#a get method to get a filtred recipe list
#endpoint = "http://127.0.0.1:8000/recipes/recipes-list/search?query=pizza"
@api_view(['GET'])
def filterd_recipe_list(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        recipes = Recipe.objects.filter(name__icontains=query)
        page_number = request.GET.get('page')
        recipes = paginated_data(recipes, page_number,6)
        return JsonResponse({"data": [recipe.to_dict() for recipe in recipes]},json_dumps_params={'indent': 4})


#get a recipe by slug
#endpoint = "http://127.0.0.1:8000/recipes/recipes-list/pesto-pizza/"
@api_view(['GET'])
def get_recipe_by_slug(request, slug):
    recipe = Recipe.objects.get(slug=slug)
    return JsonResponse(recipe.to_dict() , json_dumps_params={'indent': 4})


#a delete method to delete a recipe by slug from the database
#endpoint = "http://127.0.0.1:8000/recipes/delete/<slug>/"
@api_view(['DELETE'])
def delete_recipe_by_slug(request, slug):
    recipe = Recipe.objects.get(slug=slug)
    recipe.delete()
    return JsonResponse({"message": "recipe deleted successfully"})


#a post method to create a new recipe
#endpoint = "http://"
@swagger_auto_schema(method='post', request_body=RecipeSerializer)
@api_view(['POST'])
def create_recipe(request):
    if request.method == 'POST':
        data = request.data
        recipe = create_recipe_by_data(data = data , Recipe = Recipe)
        return JsonResponse({"data": recipe.to_dict()},json_dumps_params={'indent': 4})


#a put method to update a recipe
#endpoint = "http://"
@swagger_auto_schema(method='put', request_body=RecipeSerializer)
@api_view(['PUT'])
def update_recipe(request, slug):
    if request.method == 'PUT':
        data = request.data
        recipe = Recipe.objects.get(slug=slug)
        recipe.name = data['name']
        recipe.time = data['time']
        recipe.rating = data['rating']
        recipe.save()
        if data["images"]:
            for image in data['images']:
                recipe.images.create(url=image)
        if data["ingredients"]:
            for ingredient in data['ingredients']:
                recipe.ingredients.create(details=ingredient)
        if data["instructions"]:
            for instruction in data['instructions']:
                recipe.instructions.create(details=instruction)
        if data["vedios"]:
            for vedio in data['vedios']:
                recipe.vedios.create(url=vedio)
        recipe.save()
        return JsonResponse({"data": recipe.to_dict()},json_dumps_params={'indent': 4})