# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import SignUpForm, UserForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from .mails import send_created_account_mail
User = get_user_model()

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            send_created_account_mail(user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def edit_profile_view(request):
    user = request.user
    if user.is_anonymous:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            print("valid form? ")
            messages.success(request, 'Your profile has been successfully updated.')
            return redirect('edit_profile')  # replace 'some-view-name' with the name of the view you want to redirect to
        else:
            print("ERORS:", form.errors)
            messages.error(request, 'There was an error updating your profile. Please try again.')
    else:
        form = UserForm(instance=user, initial={'company_name': user.company_name})
    return render(request, 'edit_profile.html', context={'form': form})

@login_required
def user_data_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_anonymous:
        return HttpResponseForbidden()
    return render(request, 'user.html', context={'user':user})
