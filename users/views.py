from django.shortcuts import render,redirect
from django.contrib import messages
from profiles.models import Profile
from .forms import UserRegisterForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Dear Chef {username}, start adding your recipes..')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {
        'form' : form
    }
    return render(request, 'users/register.html', context)