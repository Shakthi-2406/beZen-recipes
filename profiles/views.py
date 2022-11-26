from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import EditProfileForm
from .models import Profile
import os
from django.shortcuts import get_object_or_404

def edit_profile(request):
    instance = get_object_or_404(Profile, user = request.user)
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance= instance)
        if form.is_valid():
            form.save()

            if len(request.FILES) != 0:
                if 'avatars' in instance.avatar.url:
                    os.remove(instance.avatar.path)
                instance.avatar = request.FILES['avatar']
            instance.save()
            return redirect('my_recipes')
    else:
        form = EditProfileForm(request.POST or None, instance= instance)
    context = {
        'form' : form,
        'instance' : instance
    }
    return render(request, 'profiles/edit_profile.html', context)

