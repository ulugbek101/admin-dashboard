from datetime import date, datetime

from django.shortcuts import render, redirect
from django.db import models


from . models import Group, Pupil
from app_users.models import User
from . import forms


def subjects(request):
    context = {
        "subjects": True,
    }
    return render(request, "app_main/subjects.html", context)


def groups(request):
    context = {
        "groups_list": Group.objects.all(),
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
        "pupils_list": Pupil.objects.all(),
        "current_date": str(date.today())[:-3],
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


def add_teacher(request):
    form = forms.TeacherForm()

    if request.method == "POST":
        form = forms.TeacherForm(request.POST, request.FILES)

        if form.is_valid():
            if request.POST.get('password1') == request.POST.get('password2'):
                teacher = form.save(commit=False)
                teacher.username = request.POST.get('email')[:request.POST.get('email').find('@')]
                teacher.set_password(request.POST.get('password2'))
                teacher.save()
                # success message: teacher added
                return redirect('teachers')
            else:
                # error message: password mismatch
                # form.fields.pop('password1')
                # form.fields.pop('password2')
                context = {
                    "form": form,
                    "title": "Yangi o'qituvchi qo'shish",
                    "btn_text": "Qo'shish",
                }
                return render(request, "form.html", context)
        else:
            # error message: form invalid
            return redirect('add_teacher')

    context = {
        "form": form,
        "title": "Yangi o'qituvchi qo'shish",
        "btn_text": "Qo'shish",
    }
    return render(request, "form.html", context)


def add_pupil(request):
    form = forms.PupilForm()

    if request.method == "POST":
        form = forms.PupilForm(request.POST)

        if form.is_valid():
            form.save()
            # success message: pupil added
            return redirect("pupils")
        else:
            # error message: form invalid
            return redirect("add-pupil")

    context = {
        "form": form,
        "title": "Yangi o'quvchi qo'shish",
        "btn_text": "Qo'shish",
    }
    return render(request, "form.html", context)
