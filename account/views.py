from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm, UserRegistrationForm, EditProfileForm, PhoneLoginform, VerifyCodeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from posts.models import Post
from django.contrib.auth.decorators import login_required
from random import randint
from kavenegar import *
from .models import Profile

def user_login(request):
    next = request.GET.get('next')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You logged in successfully', 'success')
                if next:
                    return redirect(next)
                return redirect('account:dashboard', user.id)
            else:
                messages.error(request, 'Wrong username or password!', 'warning')
    else:
        form = UserLoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            # login(request, user)
            messages.success(request, 'You registered successfully, Login now', 'success')
            return redirect('account:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


@login_required(login_url='account:login')
def user_logout(request):
    logout(request)
    messages.success(request, 'You logged out successfully', 'primary')
    return redirect('posts:all_posts')


@login_required(login_url='account:login')
def user_dashboard(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user)
    self_dash = False
    if request.user.id == user_id:
        self_dash = True
    return render(request, 'account/dashboard.html', {'user': user, 'posts': posts, 'self_dash': self_dash})


@login_required(login_url='account:login')
def edit_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request,'Your profile was edited successfully', 'success')
            return redirect('account:dashboard', user_id)
    else:
        form = EditProfileForm(instance=user.profile, initial={'email': request.user.email})
    return render(request, 'account/edit_profile.html', {'form': form})


def phone_login(request):
    if request.method == 'POST':
        form = PhoneLoginform(request.POST)
        if form.is_valid():
            phone = f"0{form.cleaned_data['phone']}"
            random_num = randint(1000,9999)
            api = KavenegarAPI('6B59357738414565307A503765434656746F4767423942726F4645466B5461374E70676E3451334479744D3D')
            params = {'sender': '', 'receptor': phone, 'message': random_num}
            api.sms_send(params)
            return redirect('account:verify', phone, random_num)
    else:
        form = PhoneLoginform()
    return render(request, 'account/phone_login.html', {'form': form})


def verify(request, phone, random_num):
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            if random_num == form.cleaned_data['code']:
                profile = get_object_or_404(Profile, phone=phone)
                user = get_object_or_404(User, profile__id=profile.id)
                login(request, user)
                messages.success(request, 'You logged in successfully', 'success')
                return redirect('posts:all_posts')
            else:
                messages.error(request, 'your code is wrong!', 'warning')
    else:
        form = VerifyCodeForm()
    return render(request, 'account/verify.html', {'form': form})
















