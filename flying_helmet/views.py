from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Recipe, Review, Cuisine, Ingredient, Ingredient_quantities
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
# Create your views here.


def index(request):
    
    return render(request, 'flying_helmet/login.html')


def signup(request):
    username, password = get_user_pass(request)
    user = User.objects.create_user(username, password=password)
    if user:
        return render(request, 'flying_helmet/home.html')
    else: 
        return index(request)

def verify(request):
    username, password = get_user_pass(request)
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        
   #     return render(request, 'homepage/home.html', context)
        return render(request, 'flying_helmet/home.html')
    else:
        return HttpResponse('Login failed.')


def get_user_pass(request):
    '''Returns username, password from POST data in request'''
    username = request.POST['username']
    password = request.POST['password']
    return username, password


def recipe(request, recipe_name):
    
    recipe = Recipe.objects.get(name=recipe_name)
    
    method = recipe.method.split('\r\n\r\n')
    quantities = recipe.ingredient_quantities_set.all()
    context = {
        'name': recipe.name, 
        'poster_username': recipe.poster_username, 
        'portions': recipe.portions, 
        'method': method,
        'prep_time': recipe.prep_time,
        'ingredients': quantities,
        'cuisine': recipe.cuisine
        }
    return render(request, 'flying_helmet/recipe.html', context)


def profile(request, poster_username):
    recipes = Recipe.objects.filter(poster_username=poster_username)
    context = {
        'name': poster_username,
        'recipes': recipes
        
    }
    return render(request, 'flying_helmet/profile.html', context)

def home(request):
    recipes = Recipe.objects.order_by('id')
    context = {
        'recipes': recipes.reverse()[:10]
    }
    return render(request, 'flying_helmet/home.html', context)

@login_required(login_url='/flying_helmet/login')
def upload(request):

    poster_username = request.user.username
    
    return render(request, 'flying_helmet/upload.html')

def post_recipe(request):
    print(request.POST)
    poster_username = request.user.username
    name = request.POST['name']

    try:
        cuisine = Cuisine.objects.get(name=request.POST['cuisine'])
    except Cuisine.DoesNotExist:
        cuisine = Cuisine(name=request.POST['cuisine'])
        cuisine.save()

    portions = request.POST['portions']
    method = request.POST['method']
    prep_time = request.POST['prep_time']
    recipe = Recipe(name=name, cuisine=cuisine, portions=portions, method=method, prep_time=prep_time, poster_username=poster_username)
    recipe.save()
    ingredients = request.POST['ingredients']
    ingredient_set = ingredients.split('\r\n')
    
    for ingredient in ingredient_set:
        ingredient_quantity = ingredient.split(':')
        print(ingredient_quantity)
        try:
            ingredient_name = ingredient_quantity[1].strip().lower()
            if not ingredient_name:
                continue
            new_ingredient = Ingredient.objects.get(name=ingredient_name)

        except Ingredient.DoesNotExist:
            
            new_ingredient = Ingredient(name=ingredient_name)   
            new_ingredient.save() 
            quantity = Ingredient_quantities(recipe=recipe, ingredient=new_ingredient, quantity=ingredient_quantity[0].strip().lower())
            quantity.save()
    messages.success(request, 'Recipe successfully added!')
    return HttpResponseRedirect(reverse('flying_helmet:upload'))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('flying_helmet:login_page'))

# /search?search=tomato&cuisine=chinese&
def search(request):
    search_term = request.GET['search']
    print(search_term)
    if not search_term:
        return HttpResponseRedirect('search?search=feihtie')
    new_terms = search_term.split(',')
    ingredients = []
    for term in new_terms:
        ingredients += list(Ingredient.objects.filter(name__contains=term.strip()))
        

    print(f'Ingredients: {ingredients}')
    recipes = Recipe.objects.filter(ingredient__in = ingredients).distinct()
    print('In rank:', recipes)
    new_recipes = filters(request, recipes)
    order = rank(ingredients, new_recipes)
    
    context = {'ingredient_recipes': order, 
        'recipes': Recipe.objects.order_by('id')[:10]}
    
    return render(request, 'flying_helmet/results.html', context)

def rank(ingredients, recipes):
    # where ingredients is in (list of ingredients)s
    ranks = []
    for recipe in recipes:
        recipe_ingredients = recipe.ingredient_set.all()
        no_of_ingredients = 0
        for ingredient in ingredients:
            if ingredient in recipe_ingredients:
                no_of_ingredients += 1
        ranks.append((recipe, no_of_ingredients))
    
    ranks.sort(reverse=True, key=lambda x:x[1])

    return [x[0] for x in ranks]
    
def filters(request, recipes):
    cuisine = request.GET.get('cuisine', '')
    if not cuisine:
        return recipes

    new_list = recipes.filter(cuisine__name=cuisine)
    return new_list

def filter(request):
    previous_url = request.META['HTTP_REFERER']
    cuisine = request.GET['cuisine']
    
    url = previous_url + '&cuisine=' + cuisine
    print('In filter')
    print('previous url:', previous_url)
    print('url:', url)
    return HttpResponseRedirect(url)
    # get the cuisine
    # get the url you have come from, and add cuisine filter to it
    # reditect to this new url
    #search?search=feihtie&cuisine=<cuisine>