from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required(login_url='account_login')
def index(request):
    return render(request, 'app_main/index.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def signin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    next_page = request.POST.get('next')

    try:
        user = User.objects.get(email=email)
    except:
        user = None

    if user:
        password_is_correct = user.check_password(password)
        if password_is_correct:
            # success message
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        else:
            # password incorrect error message
            return redirect('account_login')
    else:
        # user not found error message
        return redirect('account_login')


def signup(request):
    pass
