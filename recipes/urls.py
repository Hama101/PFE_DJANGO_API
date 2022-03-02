from django.urls import path
from . import views
from . import automated_DB as auto
app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes-list/', views.recipe_list, name='recipe_list'),
    path('recipes-list/search', views.filterd_recipe_list, name='search_recipe_list'),
    path('recipes-list/<str:slug>/', views.get_recipe_by_slug, name='get_recipe_by_slug'),
    path('delete/<str:slug>/', views.delete_recipe_by_slug, name='delete_recipe_by_slug'),
    path('create-recipe/', views.create_recipe, name='create_recipe'),
    path('update-recipe/', views.update_recipe, name='update_recipe'),

    #auto make a data base by scraping an other web site
    path('automated-DB/', auto.auto_add_recipes, name='automated_DB'),
]