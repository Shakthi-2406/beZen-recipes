from pyexpat import model
from django.forms import ModelForm
from .models import Profile
from django import forms


class EditProfileForm(ModelForm):
    email = forms.EmailField()
    avatar = forms.ImageField()

    class Meta:
        model = Profile
        fields = ['name','bio','location','email','avatar']