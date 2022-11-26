"""beZenProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import imp
from re import template
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views

from users import views as users_views
from profiles import views as profiles_views
from recipe import views as recipe_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # RECIPE
    path('', recipe_views.home, name='home'),
    path('search/', recipe_views.search, name='search_recipe'),
    path('category/<str:cat>/', recipe_views.home, name='category'),
    path('about/', recipe_views.about, name='about'),
    path('my_profile/', recipe_views.my_recipes, name='my_recipes'),
    path('profile/<str:slug>/', recipe_views.my_recipes, name='view_profile'),
    path('recipe/<int:pk>/<str:slug>/', recipe_views.view_recipe, name='view_recipe'),
    path('recipe/<int:pk>/<str:slug>/edit', recipe_views.edit_recipe, name='edit_recipe'),
    path('add_recipe/', recipe_views.add_recipe, name='add_recipe'),
    path('delete/<int:pk>', recipe_views.delete_recipe, name='delete_recipe'),
    
    

    # PROFILE
    path('edit/profile', profiles_views.edit_profile , name='edit_profile'),

    # USERS
    path('register/', users_views.register , name='register'),
    path('accounts/profile/', recipe_views.home),
    path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name='logout'),
]

urlpatterns += static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
