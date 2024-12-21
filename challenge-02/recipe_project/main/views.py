from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect,get_object_or_404
from .models import Ingredient, Recipe
from .serializers import IngredientSerializer, RecipeSerializer

@api_view(['GET', 'POST'])
def ingredients(request):
    if request.method == 'GET':
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def ingredient_detail(request, pk):
    try:
        ingredient = Ingredient.objects.get(pk=pk)
    except Ingredient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = IngredientSerializer(ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def recipes(request):
    if request.method == 'GET':
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def chat_with_bot(request):
#     message = request.GET.get('message', '')
#     if 'sweet' in message.lower():
#         suggestions = Recipe.objects.filter(taste='sweet')
#     else:
#         suggestions = Recipe.objects.all()
#     serializer = RecipeSerializer(suggestions, many=True)
#     return Response(serializer.data)

def home(request):
    return render(request, 'home.html')

def show_ingredients(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'ingredients.html', {'ingredients': ingredients})

def show_recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes.html', {'recipes': recipes})

def add_ingredient(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        unit = request.POST.get('unit')

        Ingredient.objects.create(name=name, quantity=quantity, unit=unit)

        return redirect('ingredients')  # Replace with your target URL

    return render(request, 'add_ingredient.html')


# Update ingredient view
def update_ingredient(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    
    if request.method == 'POST':
        ingredient.quantity = request.POST.get('quantity')
        ingredient.save()
        return redirect('ingredients')
       
    return render(request, 'update_ingredients.html')

def delete_ingredient(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)

    if request.method == 'POST':
        ingredient.delete()
        return redirect('ingredients')  # Redirect to the list view after deletion

    return redirect('ingredients')

def add_recipes(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')

        Recipe.objects.create(name=name, content=content)

        return redirect('recipes')  # Replace with your target URL
    
    return render(request, 'add_recipe.html')

def update_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    if request.method == 'POST':
        recipe.content= request.POST.get('content')
        recipe.save()
        return redirect('recipes')
       
    return render(request, 'update_recipes.html')

def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == 'POST':
        recipe.delete()
        return redirect('recipes')  

    return redirect('recipes')

    