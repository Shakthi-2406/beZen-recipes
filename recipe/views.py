from ast import Delete
from turtle import title
from unicodedata import category
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
import json
from django.template.defaultfilters import slugify
from recipe.models import Recipe
from django.db.models import Q
from .forms import AddRecipeForm
from django.shortcuts import get_object_or_404
from profiles.models import Profile


def home(request, cat=None):
    recipes = Recipe.objects.all().order_by('-created_at')
    veg = False
    nonveg = False
    noncat = True
    if cat:
        if cat == 'veg':
            recipes = Recipe.objects.all().filter(is_veg = True).order_by('-created_at')
            veg = True
            noncat = False
        else:
            recipes = Recipe.objects.all().filter(is_veg = False).order_by('-created_at')
            nonveg = True
            noncat = False
    context = {
        'recipes' : recipes,
        'home' : True,
        'v': veg,
        'nv': nonveg,
        'no': noncat,
        'veg': 'veg',
        'nonveg': 'nonveg'
    }
    return render(request, 'recipe/home.html', context)


def search(request,*args, **kwargs):
    q = request.GET.get('q')
    key = slugify(q)
    if key=='':
        return redirect('home')
    recipes = Recipe.objects.all().filter(Q(slug__contains = key) | Q(ingredients__contains = key)).order_by('-created_at')
    context = {
        'recipes' : recipes,
        'home' : True,
        'key': q
    }
    return render(request, 'recipe/home.html', context)

def add_recipe(request):
    title = "Add Recipe"
    add = False
    if request.user.is_authenticated:
        profinstance = get_object_or_404(Profile, user = request.user)
        r = Recipe()
        if request.method == "POST":
            form = AddRecipeForm(request.POST)
            if form.is_valid():
                if len(request.FILES) != 0:
                    r.cover = request.FILES['cover']
                r.name = request.POST.get('name')
                r.description = request.POST.get('description')
                if request.POST.get('is_veg') == 'True':
                    r.is_veg = True
                stepslst = request.POST.get('steps')
                r.steps = json.dumps(stepslst)
                inglst = request.POST.get('ingredients')
                r.ingredients = json.dumps(inglst)
                r.author = profinstance
                print(stepslst,'\n\n',inglst)
                r.save()
            return redirect('my_recipes')
        else:
            form = AddRecipeForm(request.POST or None)
        context = {
            'form' : form,
            'profile' : profinstance,
            'title': title,
            'add': add
        }
        return render(request, 'recipe/add_recipe.html', context)
    return redirect('login')

def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()
    return redirect('my_recipes')


def edit_recipe(request, pk=None, slug=None):
    r = get_object_or_404(Recipe, pk=pk)
    title = "Edit Recipe"
    add = True
    if request.method == "POST":
        form = AddRecipeForm(request.POST, instance=r)
        if form.is_valid():
            if len(request.FILES) != 0:
                r.cover = request.FILES['cover']
            r.name = request.POST.get('name')
            r.description = request.POST.get('description')
            if request.POST.get('is_veg') == 'True':
                r.is_veg = True
            stepslst = request.POST.get('steps')
            r.steps = stepslst
            
            inglst = request.POST.get('ingredients')
            r.ingredients = inglst
            r.save()
        return redirect('view_recipe',r.pk,r.slug)
    else:
        form = AddRecipeForm(request.POST or None, instance=r)
    context = {
        'form' : form,
        'title': title,
        'add': add,
        'r': r
    }
    return render(request, 'recipe/add_recipe.html', context)


def my_recipes(request, slug=None):
    own = False
    if slug == None:
        if request.user.is_authenticated:
            profile = get_object_or_404(Profile,user = request.user)
            recipes = Recipe.objects.all().filter(author = profile).order_by('-created_at')
            own = True
        else:
            return redirect('login')
    else:
        slug = slugify(slug)
        profile = get_object_or_404(Profile,slug = slug)
        recipes = Recipe.objects.all().filter(author = profile).order_by('-created_at')
    context = {
        'recipes' : recipes,
        'home' : False,
        'profilepage' : True, 
        'profile' : profile,
        'own' : own
    }
    return render(request, 'recipe/home.html', context)

def view_recipe(request, pk=None, slug=None):
    # try:
        recipe = get_object_or_404(Recipe, id=pk)
        own = False
        print(recipe.ingredients)
        # recipe.steps = recipe.steps.replace('"','').replace("\n",'').replace('\\n','').replace("\\r",'').replace("\r",'')
        recipe.steps = recipe.steps.replace('"','').replace("\n",'').replace('\\n','').replace("\\r",'').replace("\r",'')
        recipe.ingredients= recipe.ingredients.replace('"','').replace("\n",',').replace('\\n',',').replace("\\r",'').replace("\r",'')
        recipe.save()
        if ',' in recipe.ingredients:
            inglist = recipe.ingredients.split(',')
        else:
            inglist = recipe.ingredients.split('\n')
        steplist = recipe.steps.replace("\r","").replace('\n',"").split('.')
        inglist = [s for s in inglist if s != "" and s!= " " and s!=None]
        print(steplist)
        steplist = [s for s in steplist if s != "" and s!= " " and s!=None]
        if recipe.author.user == request.user:
            own = True
        recipes = Recipe.objects.all().filter(author = recipe.author)
        context = {
            'recipes' : recipes,
            'r': recipe,
            'own' : own,
            'inglist': inglist,
            'steplist': steplist
        }
        return render(request, 'recipe/view_recipe.html', context)
    # except:
    #     return redirect('home')
    


def about(request):
    context = {
        
    }
    return render(request, 'recipe/about.html', context)