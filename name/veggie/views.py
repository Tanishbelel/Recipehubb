from django.shortcuts import render, redirect,get_object_or_404

from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from datetime import timedelta, date
from django.db.models import Q
from django.db.models import Count
from .models import Recipe, Favorite
from django.http import JsonResponse


# Create your views here.
@login_required(login_url = '/login/')
def recipes(request):
    if request.method == "POST":
        data=request.POST
        recipe_name = data.get('recipe_name')
        recipe_des = data.get('recipe_des')
        recipe_image = request.FILES.get('recipe_image')

        Recipe.objects.create(
           recipe_des = recipe_des,
           recipe_image = recipe_image,
           recipe_name = recipe_name,
       )
        
        return redirect('/recipes/')
    queryset = Recipe.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(recipe_name__icontains = request.GET.get('search'))

    context = {'recipes': queryset}
        
    return render(request , "recipes.html", context)


def delete(request,id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/recipes/')

def update(request,id):
    queryset = Recipe.objects.get(id=id)
    if request.method == "POST":
       data = request.POST
       recipe_name = data.get('recipe_name')
       recipe_des = data.get('recipe_des')
       recipe_image = request.FILES.get('recipe_image')

       queryset.recipe_name = recipe_name
       queryset.recipe_des = recipe_des

       if recipe_image:
           queryset.recipe_image = recipe_image
           queryset.save()
           return redirect('/recipes/')


    context = {'recipes': queryset}
    return render(request , "update.html", context)


def login_page(request):
    if request.method== "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
             messages.info(request, 'Invalid Data')
             return redirect('/login/')
        user = authenticate(username = username, password = password)

        if user is None:
             messages.info(request, 'Invalid Data')
             return redirect('/login/')
        else :
            login(request, user)
            return redirect('/recipes/')

    return render(request, 'login.html')
    

def register_page(request):

    if request.method== "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, 'Username already Taken')
            return redirect('/register/')

        user=User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        user.set_password(password)
        user.save()


        messages.info(request, 'Account Created Successfully')

        return redirect("/register/")

    return render(request, 'register.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

@login_required(login_url='/login/')
def dashboard(request):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())

    # Calculate statistics for the dashboard
    recipes_added_this_week = Recipe.objects.filter(created_at__gte=start_of_week).count()
    recipes_without_images = Recipe.objects.filter(recipe_image=None).count()
    total_recipes = Recipe.objects.count()

    context = {
        'recipes_added_this_week': recipes_added_this_week,
        'recipes_without_images': recipes_without_images,
        'total_recipes': total_recipes
    }

    return render(request, 'dashboard.html', context)

@login_required
def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        recipe=recipe,
    )
    
    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True
    
    return JsonResponse({
        'status': 'success',
        'is_favorite': is_favorite
    })

@login_required
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('recipe')
    return render(request, 'favs.html', {'favorites': favorites})
@login_required
def favorites_view(request):
    # Get all recipes that the current user has favorited
    favorite_recipes = Recipe.objects.filter(
        favorite__user=request.user
    ).select_related()
    
    return render(request, 'favs.html', {
        'recipes': favorite_recipes
    })
def home(request):
    # Get featured recipes (latest 6 recipes)
    featured_recipes = Recipe.objects.select_related('user').order_by('-id')[:6]
    
    # Get all categories
    categories = Category.objects.all()
    
    # Get user's favorite recipes if logged in
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Recipe.objects.filter(
            favorite__user=request.user
        )
    
    context = {
        'featured_recipes': featured_recipes,
        'categories': categories,
        'user_favorites': user_favorites,
    }
    
    return render(request, 'index.html', context)