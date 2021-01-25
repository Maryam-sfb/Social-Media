from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from posts.models import Post
from django.contrib.auth.decorators import login_required


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













