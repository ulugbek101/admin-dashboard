from datetime import date, datetime

from django.shortcuts import render, redirect
from django.db.models import Count, Sum


from . models import Group, Pupil, Payment, Subject
from app_users.models import User
from . import forms


def subjects(request):
    context = {
        "subjects": True,
        "subjects_list": Subject.objects.annotate(pupils=Count("group__pupil")).order_by("name", "-created")
    }
    return render(request, "app_main/subjects.html", context)


def groups(request):
    context = {
        "groups_list": Group.objects.all().order_by("name", "-created"),
        "groups": True,
    }
    return render(request, "app_main/groups.html", context)


def teachers(request):
    context = {
        "teachers": True,
        "teachers_list": User.objects.all().order_by("last_name", "first_name", "-created")
    }
    return render(request, "app_main/teachers.html", context)


def pupils(request):
    context = {
        "pupils_list": Pupil.objects.all().order_by("last_name", "first_name", "-created"),
        "current_date": str(date.today())[:-3],
        "pupils": True,
    }
    return render(request, "app_main/pupils.html", context)


def dashboard(request):
    total_payment = Group.objects.aggregate(total_amount=Sum("price")).get("total_amount")
    total_paid = Payment.objects.aggregate(paid_amount=Sum("amount")).get("paid_amount")

    context = {
        "dashboard": True,
        "total_payment": total_payment,
        "total_paid": total_paid,
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
                teacher.username = request.POST.get(
                    'email')[:request.POST.get('email').find('@')]
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
            return redirect("add_pupil")

    context = {
        "form": form,
        "title": "Yangi o'quvchi kiritish",
        "btn_text":  "Kiritish",
    }
    return render(request, "form.html", context)


def add_payment(request, group_id, pupil_id):
    try:
        payment = Payment.objects.get(pupil__id=pupil_id, month__month=date.today().month)
    except:
        payment = None
    
    form = forms.PaymentForm(data={
        'amount': payment.amount if payment else 0,
    })
    pupil = Pupil.objects.get(group__id=group_id, id=pupil_id)

    if request.method == 'POST':
        if payment:
            form = forms.PaymentForm(request.POST, instance=payment)
        else:
            form = forms.PaymentForm(request.POST)

        if form.is_valid():
            if request.POST.get('amount') == '0':
                # error message: payment cannot be equal to 0
                return redirect("add_payment", group_id=group_id, pupil_id=pupil_id)

            if int(request.POST.get('amount')) > pupil.group.price:
                # error message: payment is more than group price
                return redirect("add_payment", group_id=group_id, pupil_id=pupil_id)

            payment = form.save(commit=False)
            payment.owner = request.user
            payment.pupil = pupil
            payment.group = pupil.group
            payment.save()
            # success message: payment added
            return redirect("pupils")
        else:
            # error message: invalid payment form
            return redirect("add_payment", group_id=group_id, pupil_id=pupil_id)

    context = {
        "form": form,
        "title": f"{Pupil.objects.get(id=pupil_id).full_name} ga {Group.objects.get(id=group_id).name} guruhi uchun to'lov kiritish",
        "btn_text": "To'lovni kiritish",
        "max_payment": pupil.group.price,
    }
    return render(request, "form.html", context)


def add_group(request):
    form = forms.GroupForm()

    if request.method == 'POST':
        form = forms.GroupForm(request.POST)

        if form.is_valid():
            form.save()
            # success message: group created
            return redirect('groups')
        else:
            # error message: price should be more than 0
            return redirect('add_group')

    context = {
        "form": form,
        "title": "Guruh qo'shish",
        "btn_text": "Guruhni qo'shish"
    }
    return render(request, "form.html", context)


def add_subject(request):

    if request.method == "POST":
        form = forms.SubjectForm(request.POST)

        if form.is_valid():
            form.save()
            # success message: subject added
            return redirect("subjects")
        else:
            # error message: form invalid
            return redirect("add_subject")

    form = forms.SubjectForm()
    context = {
        "form": form,
        "title": "Fan qo'shish",
        "btn_text": "Fanni qo'shish"
    }
    return render(request, "form.html", context)


def update_pupil(request, pk):
    pupil = Pupil.objects.get(id=pk)
    form = forms.PupilForm(instance=pupil)

    if request.method == 'POST':
        form = forms.PupilForm(request.POST, instance=pupil)

        if form.is_valid():
            form.save()
            # success message: pupil updated
            return redirect("pupils")
        else:
            # error message: form invalid e.g: pupil with the same first name, last name and group name
            return redirect("update_pupil", pk=pk)

    context = {
        "form": form,
        "title": "O'quvchi ma'lumotlarini o'zgartirish",
        "btn_text": "O'quvchi ma'lumotlarini yangilash"
    }
    return render(request, "form.html", context)


def update_teacher(request, pk):
    teacher = User.objects.get(id=pk)
    form = forms.TeacherForm(instance=teacher)

    if request.method == 'POST':
        form = forms.TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            # success message: teacher updated
            return redirect("teachers")
        else:
            # error message: form invalid e.g: teacher should have first and last names
            return redirect("update_teacher", pk=pk)

    context = {
        "form": form,
        "title": "O'qituvchi ma'lumotlarini o'zgartirish",
        "btn_text": "O'qituvchi ma'lumotlarini yangilash"
    }
    return render(request, "form.html", context)


def update_group(request, pk):
    group = Group.objects.get(id=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        teacher = User.objects.get(id=request.POST.get('teacher'))
        subject = Subject.objects.get(id=request.POST.get('subject'))

        if name and teacher and subject:
            group.name = name
            group.teacher = teacher
            group.subject = subject
            group.save()
            # success message: group information has changed
            return redirect('groups')
        else:
            # error message: invalid form
            return redirect('update_group', pk=pk)

    form = forms.GroupForm(instance=group)
    form.fields.pop('price')
    context = {
        "form": form,
        "title": "Guruh ma'lumotlarini o'zgartirish",
        "btn_text": "Guruh ma'lumotlarini yangilash"
    }
    return render(request, "form.html", context)


def update_subject(request, pk):
    subject = Subject.objects.get(id=pk)

    if request.method == "POST":
        form = forms.SubjectForm(request.POST, instance=subject)

        if form.is_valid():
            form.save()
            # success message: subject added
            return redirect("subjects")
        else:
            # error message: form invalid
            return redirect("update_subject", pk=pk)

    form = forms.SubjectForm(instance=subject)
    context = {
        "form": form,
        "title": "Fan qo'shish",
        "btn_text": "Fanni qo'shish"
    }
    return render(request, "form.html", context)


def delete_pupil(request, pk):
    pupil = Pupil.objects.get(id=pk)

    if request.method == 'POST':
        pupil.delete()
        # success message: pupil deleted
        return redirect("pupils")

    context = {
        "title": pupil.full_name,
    }
    return render(request, "delete.html", context)


def delete_teacher(request, pk):
    teacher = User.objects.get(id=pk)

    if request.method == 'POST':
        teacher.delete()
        # success message: pupil deleted
        return redirect("teachers")

    context = {
        "title": teacher.full_name,
    }
    return render(request, "delete.html", context)


def delete_group(request, pk):
    group = Group.objects.get(id=pk)

    if request.method == 'POST':
        group.delete()
        # success message: group deleted
        return redirect("groups")

    context = {
        "title": group.name,
    }
    return render(request, "delete.html", context)


def delete_subject(request, pk):
    subject = Subject.objects.get(id=pk)

    if request.method == 'POST':
        subject.delete()
        # success message: subject deleted
        return redirect("subjects")

    context = {
        "title": subject.name,
    }
    return render(request, "delete.html", context)
