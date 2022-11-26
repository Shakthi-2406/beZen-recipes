from django import forms
from django.forms import ModelForm
from .models import Recipe

class AddRecipeForm(ModelForm):
    prept = forms.IntegerField(required=True)
    cookt = forms.IntegerField(required=True)
    servings = forms.IntegerField(required=True)
    class Meta:
        model = Recipe
        fields = ['name','description','ingredients','steps','is_veg','prept','cookt','servings','cover']