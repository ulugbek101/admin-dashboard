from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, get_user_model
from django.contrib import messages

User = get_user_model()


def signout(request):
    messages.info(request, "Tizimdan chiqdingiz")
    logout(request)
    return redirect("signin")


def signin(request):
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
