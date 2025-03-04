from django.shortcuts import render

# Create your views here.

# users/views.py
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})
