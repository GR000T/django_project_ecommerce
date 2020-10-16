from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import (
                authenticate,
                get_user_model,
                login,
                logout
)
from django.contrib.auth.models import User
from store.models import Customer
from .forms import UserLoginForm,UserRegisterForm
from django.contrib import messages
from django.urls import reverse

@csrf_exempt
def register(request):
    form=UserRegisterForm()
    if(request.method=="POST"):
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            password=form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            messages.success(request,'Account Created')
            return redirect('login')
    context={'form':form}
    return render(request,'accounts/register.html',context)

@csrf_exempt
def login_view(request):
    form=UserLoginForm()
    
    if(request.method=="POST"):
        
        #form=UserLoginForm(request.POST)
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('store')

    context={'form':form}
    return render(request,'accounts/login.html',context)

@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('store')
