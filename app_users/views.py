from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


def signout(request):
    logout(request)
    return redirect("signin")


def signin(request):

    if request.method == 'POST':
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
                # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                login(request, user)
                
                if next_page:
                    return redirect(next_page)

                return redirect('dashboard')
            else:
                # password incorrect error message
                return redirect('signin')
        else:
            # user not found error message
            return redirect('signin')
    
    context = {}
    return render(request, "app_users/signin.html", context)


def signup(request):
    context = {}
    return render(request, "app_users/signup.html", context)
