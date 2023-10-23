from django.shortcuts import render


from app_users.models import User


def subjects(request):
    context = {
        "subjects": True,
    }
    return render(request, "app_main/subjects.html", context)


def groups(request):
    context = {
        "groups": True,
    }
    return render(request, "app_main/groups.html", context)


def teachers(request):
    context = {
        "teachers": True,
        "teachers_list": User.objects.all().order_by('created')
    }
    return render(request, "app_main/teachers.html", context)


def pupils(request):
    context = {
        "pupils": True,
    }
    return render(request, "app_main/pupils.html", context)


def dashboard(request):
    context = {
        "dashboard": True,
    }
    return render(request, "app_main/dashboard.html", context)


def settings(request):
    context = {
        "settings": True,
    }
    return render(request, "app_main/settings.html", context)
