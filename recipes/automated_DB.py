'''
    in this file we will be reading urls from the cards.txt
    and then we will be creating a recipe form each url of the card by sending a post request to the create_recipe endpoint
    and we get the data from the flask server !
    endpoint = https://sea-of-food.herokuapp.com/recipe-details
    request = {"url": "https://www.allrecipes.com/recipe/2359/chicken-and-rice-salad/"}
    response = ...
    
'''

from django.http import JsonResponse
from .models import Recipe
import requests
from rest_framework.decorators import api_view
import time

from .utils import create_recipe_by_data

def auto_add_one_recipe(url , user):
    #get the data from the server we host with the flask server 
    endpoint = "https://sea-of-food.herokuapp.com/recipe-details"
    reqest_body = {'url':f'{url}'}
    response = requests.post(endpoint, json=reqest_body)
    data = response.json()

    try:
        data = data['data']
    except KeyError as e:
        print("error in the data")
        pass

    #create an instance of the recipe model
    recipe = create_recipe_by_data(data = data , Recipe = Recipe , user = user)
    print("Created a new recipe ", recipe.slug)
    pass


@api_view(['GET'])
def auto_add_recipes(request):
    #check if the request user is an admin
    print(request.user)
    if not request.user.is_superuser:
        return JsonResponse({"message":"you are not allowed to do this"})

    #read lines from urls.txt and for each line call auto_add_one_recipe
    #read lines from the done.txt
    done_urls = []
    with open("done.txt", "r") as f:
        for line in f:
            done_urls.append(line.strip())

    with open('urls.txt' , 'r') as f:
        for line in f:
            url = line.strip()
            if url not in done_urls:
                try:
                    auto_add_one_recipe(url, request.user)
                except Exception as e:
                    pass
                #write the line in done.txt
                with open('done.txt' , 'a') as done:
                    done.write(line)


    return JsonResponse({"message": "recipes added successfully"})