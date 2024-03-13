from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, get_user_model
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse

from . import utils

User = get_user_model()


def send_sms(request):
    print(request)
    if request.method == 'GET':    
        # Send SMS to pupils
        return utils.send_sms_to_pupils(request)
    
    return JsonResponse(data={'detail': 'Method is not allowed'})


# class CustomLogoutView(LogoutView):
#     def get_success_url(self):
#         messages.info(self.request, "Tizimdan chiqdingiz")
#         return reverse("signin")

def signout(request):
    logout(request)
    messages.info(request, "Tizmindan chiqdingiz")
    return redirect("signin")

def signin(request):
    if request.user.is_authenticated:
        messages.info(request, 'Boshqa akkauntga kirish uchun avval tizimdan chiqing')
        return redirect('groups')

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        next_page = request.POST.get("next")

        try:
            user = User.objects.get(email=email)
        except:
            user = None

        if user:
            password_is_correct = user.check_password(password)
            if password_is_correct:
                messages.success(request, f"Xush kelibsiz, {user.first_name} {user.last_name}!")
                # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                login(request, user)

                if next_page:
                    return redirect(next_page)

                return redirect("groups")
            else:
                messages.error(request, "Parol noto'g'ri kiritilgan")
                context = {
                    "title": "Tizimga kirish",
                    "email": email,
                }
                return render(request, "app_users/signin.html", context)
        else:
            messages.error(request, "Bunday foydalanuvhi tizimda topilmadi")
            context = {
                "title": "Tizimga kirish",
                "email": email,
            }
            return render(request, "app_users/signin.html", context)

    context = {
        "title": "Tizimga kirish",
    }
    return render(request, "app_users/signin.html", context)


def signup(request):
    context = {}
    return render(request, "app_users/signup.html", context)
