from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    
    path('',home, name= 'home'),
    path('ingredients/',show_ingredients, name= 'ingredients'),
    path('add_ingredient/', add_ingredient, name ='add_ingredient'),
    path('update_ingredient/<int:ingredient_id>', update_ingredient, name ='update_ingredient' ),
    path('delete_ingredient/<int:ingredient_id>',delete_ingredient, name= 'delete_ingredient' ),
    path('recipes/',show_recipes, name= 'recipes'),
    path('add_recipes/', add_recipes, name ='add_recipes'),
    path('update_recipe/<int:recipe_id>', update_recipe, name ='update_recipe' ),
    path('delete_recipe/<int:recipe_id>',delete_recipe, name= 'delete_recipe' ),
    # path('dashboard/', dashboard_view, name='dashboard'),

    path('generate-recipe/', generate_recipe, name="generate_recipe"),
    path('chatbot/', chatbot_view, name="chatbot"),

    path('chatbot-reply/<str:message>/', chatbot_reply, name='chatbot_reply'),

]
