from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, CreateView
from openpyxl import Workbook

from app_users.models import User
from . import forms
from . import utils
from .decorators import is_superuser
from .models import Group, Pupil, Payment, Subject, Expense


class SubjectList(LoginRequiredMixin, ListView):
    """Return subjects list"""
    template_name = "app_main/subjects.html"
    context_object_name = "subjects_list"

    def get_queryset(self):
        """
        Return subjects list if user is superuser,
        otherwise throw 404 error
        """
        subjects = Subject.objects.annotate(pupils=Count("group__pupil"))
        if not self.request.user.is_superuser:
            raise Http404("Not found")
        return subjects


class GroupList(LoginRequiredMixin, ListView):
    template_name = "app_main/groups.html"
    context_object_name = "groups_list"

    extra_context = {
        "title": "Barcha guruhlar",
        "groups": True,
    }

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Group.objects.all()
        return Group.objects.filter(teacher=self.request.user).order_by("name", "-created")


class GroupDetail(LoginRequiredMixin, DetailView):
    model = Group
    template_name = "app_main/group_detail.html"
    pk_url_kwarg = "id"
    context_object_name = "group"

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser and self.request.user != self.get_object().teacher:
            raise Http404("Not found")
        return super(GroupDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GroupDetail, self).get_context_data(**kwargs)
        context["pupils"] = Pupil.objects.filter(group=self.object)
        context["group_id"] = self.object.id
        context["title"] = self.object.name
        return context


class TeacherList(LoginRequiredMixin, ListView):
    """Return teachers list"""

    queryset = User.objects.all().order_by("last_name", "first_name", "-created")
    template_name = "app_main/teachers.html"
    context_object_name = "teachers_list"
    extra_context = {
        "title": "Barcha o'qituvchilar",
        "teachers": True,
    }


class PupilList(LoginRequiredMixin, ListView):
    """Return students list"""

    template_name = "app_main/pupils.html"
    context_object_name = "pupils_list"
    extra_context = {
        "title": "Barcha o'quvchilar",
        "current_date": str(date.today())[:-3],
        "pupils": True
    }

    def get_queryset(self):
        """
        Return all students if user is superuser,
        otherwise only students of the teacher
        """

        pupils = Pupil.objects.all().order_by(
            "group__name", "first_name", "last_name", "-created"
        )
        if not self.request.user.is_superuser:
            return pupils.filter(group__teacher=self.request.user)
        return pupils


class ExpenseList(LoginRequiredMixin, ListView):
    """Render expenses list"""

    template_name = "app_main/expenses.html"
    context_object_name = "expenses_list"
    extra_context = {
        "title": "Chiqimlar ro'yxati",
        "expenses": True
    }

    def get_queryset(self):
        """
        Return all expenses if user is superuser,
        otherwise only expenses of the user
        """

        expenses = Expense.objects.all().order_by("-created")
        if not self.request.user.is_superuser:
            return expenses.filter(owner=self.request.user)
        return expenses


class ExpenseDetail(LoginRequiredMixin, DetailView):
    """Renders a page with detailed information about certain expense"""

    template_name = "app_main/expense_detail.html"
    model = Expense
    context_object_name = "expense"
    pk_url_kwarg = "expense_id"

    def dispatch(self, request, *args, **kwargs):
        """
        Return an expense if user is a creator or superuser of this object,
        otherwise throws 404 error
        """

        if not self.request.user.is_superuser and self.get_object().owner == self.request.user:
            raise Http404("Not found")
        return super(ExpenseDetail, self).dispatch(request, *args, **kwargs)


@login_required(login_url="signin")
@is_superuser
def dashboard(request):
    groups = Group.objects.all()
    total_paid, total_payment = utils.get_payment_info(
        year=date.today().year, month=date.today().month
    )

    payments = Payment.objects.filter(month__lte=date.today()).order_by("created")

    months = utils.get_months()

    payments_dataset = dict.fromkeys(months.values(), 0)

    for payment in payments:
        if payment.month.year == date.today().year:
            payment_month = payment.month.month
            if months[payment_month] not in payments_dataset:
                payments_dataset[months[payment_month]] = payment.amount
            else:
                payments_dataset[months[payment_month]] += payment.amount

    for month_number in months.keys():
        if month_number > date.today().month:
            payments_dataset.pop(months[month_number])

    context = {
        "title": "Analitika",
        "dashboard": True,
        "total_payment": total_payment,
        "total_paid": total_paid,
        "months_list": list(payments_dataset.keys()),
        "payments_list": list(payments_dataset.values()),
        "groups_total_payments": [group.get_total_payment for group in groups],
        "groups_names": [group.name for group in groups],
    }
    return render(request, "app_main/dashboard.html", context)


@login_required(login_url="signin")
def download_stats(request):
    months = utils.get_months()
    month = request.POST.get("month")
    year = date.today().year

    pupils = Pupil.objects.all().order_by(
        "group__name", "first_name", "last_name", "-created"
    )

    if month == "current":
        month = date.today().month
    else:
        month = date.today().month - 1
        if month < 1:
            year -= 1
            month = 12

    total_paid, total_payment = utils.get_payment_info(year=year, month=month)

    wb = Workbook(write_only=True)
    ws = wb.create_sheet()
    ws.append(["№", "Guruh", "O'quvchi", "Oy", "To'lov", "Izoh"])

    for index, pupil in enumerate(pupils, start=1):
        if (pupil.created.year == year and pupil.created.month <= month) or (
                pupil.created.year < year
        ):
            pupil_payment = pupil.payment_set.filter(
                month__year=year, month__month=month
            )

            if pupil_payment:
                group_name_ = (
                    pupil_payment[0].group.name
                    if pupil_payment[0].group
                    else pupil_payment.group_name
                )
                pupil_name_ = (
                    pupil_payment[0].pupil.full_name
                    if pupil_payment[0].pupil
                    else pupil_payment.pupil_fullname
                )
                month_ = months[month]
                amount_ = f"{pupil_payment[0].amount} / {pupil.group.price}"
                note_ = pupil_payment[0].note if pupil_payment[0].note else "-"
            else:
                group_name_ = pupil.group.name
                pupil_name_ = pupil.full_name
                month_ = months[month]
                amount_ = f"{0} / {pupil.group.price}"
                note_ = "-"

            ws.append([index, group_name_, pupil_name_, month_, amount_, note_])

    ws.append(["", "", "", "", f"{total_paid} / {total_payment}", ""])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response[
        "Content-Disposition"
    ] = f"attachment; filename={months[month]}-{year}-statistikasi.xlsx"
    wb.save(response)

    return response


@login_required(login_url="signin")
def settings(request):
    if request.method == "POST":
        password1, password2, first_name, last_name, email, profile_picture, job = (
            request.POST.get("password1"),
            request.POST.get("password2"),
            request.POST.get("first_name"),
            request.POST.get("last_name"),
            request.FILES.get("email"),
            request.FILES.get("profile_picture"),
            request.FILES.get("job"),
        )
        if first_name and last_name:
            user = request.user
            user.first_name = first_name
            user.last_name = last_name

            if email:
                user.email = email
            if profile_picture:
                user.profile_picture = profile_picture
            if job:
                user.job = job

            password_error_message = ""
            if (password1 and password2) and (password1 == password2):
                if len(password1) >= 8:
                    messages.info(request, "Parol o'zgartirildi")
                    user.set_password(request.POST.get("password2"))
                else:
                    password_error_message = "Parol 8 ta belgidan uzun bo'lishi shart"

            user.save()
            messages.success(request,
                             "Profil ma'lumotlari yangilandi") if not password_error_message else messages.error(
                request, password_error_message)
            return redirect("settings")
        else:
            messages.success(request, "Forma noto'g'ri to'ldirilgan")
            return redirect("settings")

    context = {
        "title": "Sozlamalar",
        "settings": True,
        "btn_text": "Profile ma'lumotlarini yangilash",
    }
    return render(request, "app_main/settings.html", context)


class TeacherCreate(LoginRequiredMixin, CreateView):
    model = User
    template_name = "form.html"
    success_url = reverse_lazy("teachers")
    form_class = forms.TeacherForm
    extra_context = {
        "title": "Yangi o'qituvchi qo'shish",
        "btn_text": "Qo'shish",
    }

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404("Not found")
        return super(TeacherCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password1 = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")

        if password1 == password2:
            teacher = form.save(commit=False)
            teacher.username = self.request.POST.get("email")[
                               : self.request.POST.get("email").find("@")
                               ]
            teacher.set_password(password2)
            teacher.save()

            messages.success(self.request, "O'qituvchi qo'shildi")
            return redirect("teachers")
        else:
            messages.error(self.request, "Parollar bir xil bo'lishi shart")
            return super(TeacherCreate, self).form_invalid(form)


class PupilCreate(LoginRequiredMixin, CreateView):
    """Render form that creates student"""

    template_name = "form.html"
    form_class = forms.PupilForm
    extra_context = {
        "title": "Yangi o'quvchi qo'shish",
        "btn_text": "Kiritish",
    }

    def dispatch(self, request, *args, **kwargs):
        """
        Render form if user is the owner of the group,
        otherwise throw 404 error
        """

        group = get_object_or_404(Group, id=self.request.GET.get('group_id'))
        if self.request.user != group.teacher and not self.request.user.is_superuser:
            raise Http404("Not found")
        return super(PupilCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        group = get_object_or_404(Group, id=self.request.GET.get("group_id"))
        pupil = form.save(commit=False)
        pupil.group = group
        pupil.save()
        return redirect("group_detail", id=group.id)


@login_required(login_url="signin")
def add_payment(request, group_id, pupil_id):
    pupil = Pupil.objects.get(id=pupil_id)

    if not request.user.is_superuser and request.user != pupil.group.teacher:
        messages.error(request, "Boshqalarning o'quvchisini uchun to'lov qila olmaysiz")
        return redirect("groups")

    try:
        payment = Payment.objects.get(
            pupil__id=pupil_id, month__month=date.today().month
        )
    except:
        payment = None

    # If there is an existing payment, add note field to display it in the form
    if payment:
        form = forms.PaymentForm(
            data={
                "amount": payment.amount if payment else 0,
                "note": payment.note if payment.note else "",
            }
        )
    # Otherwise display a form with blank note field
    else:
        form = forms.PaymentForm(
            data={
                "amount": payment.amount if payment else 0,
            }
        )

    pupil = Pupil.objects.get(group__id=group_id, id=pupil_id)

    if request.method == "POST":
        if payment:
            form = forms.PaymentForm(request.POST, instance=payment)
        else:
            form = forms.PaymentForm(request.POST)

        if form.is_valid():
            if request.POST.get("amount") == "0":
                messages.error(request, "To'lov miqdori 0 bo'lishi mumkin emas")
                return redirect("add_payment", group_id=group_id, pupil_id=pupil_id)

            if int(request.POST.get("amount")) > pupil.group.price:
                messages.error(request, "Qo'lov miqdori guruh to'lovi moiqdoridan ko'p")
                return redirect("add_payment", group_id=group_id, pupil_id=pupil_id)

            payment = form.save(commit=False)
            payment.owner = request.user
            payment.pupil = pupil
            payment.group = pupil.group
            payment.save()
            messages.success(request, "To'lov amalga oshirildi")
            return redirect("pupils")
        else:
            messages.error(request, "Forma noto'g'ri to'ldirilgan")
            return redirect("add_payment", group_id=group_id, pupil_id=pupil_id)

    form.fields["month"].widget.attrs.update({"value": date.today()})
    context = {
        "title": "To'lov qo'shish",
        "form": form,
        "title": f"{Pupil.objects.get(id=pupil_id).full_name} ga {Group.objects.get(id=group_id).name} guruhi uchun to'lov kiritish",
        "btn_text": "To'lovni kiritish",
        "max_payment": pupil.group.price,
    }
    return render(request, "form.html", context)


@login_required(login_url="signin")
def add_group(request):
    form = forms.GroupForm()

    if request.method == "POST":
        form = forms.GroupForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Guruh yaratildi")
            return redirect("groups")
        else:
            messages.error(request, "Guruh to'lovi miqdori 0 bo'lishi mumkin emas")
            return redirect("add_group")

    context = {
        "form": form,
        "title": "Guruh qo'shish",
        "btn_text": "Guruhni qo'shish",
    }
    return render(request, "form.html", context)


class GroupCreate(LoginRequiredMixin, CreateView):
    """Render form that creates group"""

    template_name = "form.html"
    form_class = forms.GroupForm
    success_url = reverse_lazy("groups")
    extra_context = {
        "title": "Guruh qo'shish",
        "btn_text": "Guruhni qo'shish",
    }

    def form_valid(self, form):
        messages.success(self.request, "Guruh yaratildi")
        return super(GroupCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Guruh to'lovi miqdori 0 bo'lishi mumkin emas")
        return super(GroupCreate, self).form_invalid(form)


class SubjectCreate(LoginRequiredMixin, CreateView):
    """Render form that creates subject"""

    template_name = "form.html"
    form_class = forms.SubjectForm
    success_url = reverse_lazy("subjects")
    extra_context = {
        "title": "Fan qo'shish",
        "btn_text": "Fanni qo'shish",
    }

    def dispatch(self, request, *args, **kwargs):
        """
        Render form that creates subject if user is superuser,
        otherwise throw 404 error
        """

        if not self.request.user.is_superuser:
            raise Http404("Not found")
        return super(SubjectCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Fan qo'shildi")
        return super(SubjectCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Bunday fan allaqachon mavjud")
        return super(SubjectCreate, self).form_invalid(form)


class ExpenseCreate(LoginRequiredMixin, CreateView):
    """Render form that creates expense"""

    template_name = "form.html"
    form_class = forms.ExpenseForm
    success_url = reverse_lazy("expenses")
    extra_context = {
        "title": "Chiqim qo'shish",
        "btn_text": "Chiqimni qo'shish",
    }

    def form_valid(self, form):
        expense = form.save(commit=False)
        expense.owner = self.request.user
        expense.save()

        messages.success(self.request, "Chiqim qo'shildi")
        return redirect("expenses")

    def form_invalid(self, form):
        messages.error(self.request, "Forma noto'g'ri to'ldirilgan")
        return super(ExpenseCreate, self).form_invalid(form)


class PupilUpdate(LoginRequiredMixin, UpdateView):
    template_name = "form.html"
    model = Pupil
    form_class = forms.PupilForm
    pk_url_kwarg = "pk"
    success_url = reverse_lazy("pupils")

    extra_context = {
        "title": "O'quvchi ma'lumotlarini o'zgartirish",
        "btn_text": "O'quvchi ma'lumotlarini yangilash",
    }

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser and self.request.user != self.get_object().group.teacher:
            raise Http404("Not found")
        return super(PupilUpdate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "O'quvchi ma'lumotlari yangilandi")
        return super(PupilUpdate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Forma noto'g'ri to'ldirilgan. Bundan ma'lumotlarga ega o'quvchi mavjud")
        return super(PupilUpdate, self).form_invalid(form)


class TeacherUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "form.html"
    form_class = forms.TeacherForm
    pk_url_kwarg = "pk"
    success_url = reverse_lazy("teachers")

    extra_context = {
        "title": "O'qituvchi ma'lumotlarini o'zgartirish",
        "btn_text": "O'qituvchi ma'lumotlarini yangilash",
    }

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser and self.request.user != self.get_object():
            raise Http404("Not found")
        return super(TeacherUpdate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password1 = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")
        teacher = self.object

        if (password1 or password2) and (password1 == password2):
            teacher.set_password(password2)
            teacher.save()

            messages.success(self.request, "O'qituvchi ma'lumotlari yangilandi")
            return redirect("teachers")
        else:
            messages.error(self.request, "Parollar bir xil bo'lishi shart")
            return redirect("update_teacher", pk=teacher.id)

    def form_invalid(self, form):
        messages.error(self.request, "O'qituvchi ism va familiyaga ega bo'lishi shart")
        return super(TeacherUpdate, self).form_invalid(form)


@login_required(login_url="signin")
def update_group(request, pk):
    group = get_object_or_404(Group, pk=pk)

    if request.method == "POST":
        name = request.POST.get("name")

        # Get those fields only if user is admin
        if request.user.is_superuser:
            teacher = User.objects.get(id=request.POST.get("teacher"))
            subject = Subject.objects.get(id=request.POST.get("subject"))

        if name:
            group.name = name

            # if user is admin
            if request.user.is_superuser:
                # if user is admin and did not provide teacher and subject
                if not teacher and not subject:
                    messages.error(request, "Forma noto'g'ri to'ldirilgan")
                    return redirect("update_group", pk=pk)
                # If everything is good
                group.teacher = teacher
                group.subject = subject

            group.save()
            messages.success(request, "Guruh ma'lumotlari yangilandi")
            return redirect("groups")
        else:
            messages.error(request, "Forma noto'g'ri to'ldirilgan")
            return redirect("update_group", pk=pk)

    form = forms.GroupForm(instance=group)
    form.fields.pop("price")

    if not request.user.is_superuser:
        form.fields.pop("subject")
        form.fields.pop("teacher")

    context = {
        "form": form,
        "title": "Guruh ma'lumotlarini o'zgartirish",
        "btn_text": "Guruh ma'lumotlarini yangilash",
    }
    return render(request, "form.html", context)


@login_required(login_url="signin")
def update_subject(request, pk):
    subject = Subject.objects.get(id=pk)

    if request.method == "POST":
        form = forms.SubjectForm(request.POST, instance=subject)

        if form.is_valid():
            form.save()
            messages.success(request, "Fan qo'shildi")
            return redirect("subjects")
        else:
            messages.error(request, "Forma noto'g'ri to'ldirilgan")
            return redirect("update_subject", pk=pk)

    form = forms.SubjectForm(instance=subject)
    context = {
        "title": "Fan ma'lumotlarini yangilash",
        "form": form,
        "btn_text": "Fanni qo'shish",
    }
    return render(request, "form.html", context)


class PupilDelete(LoginRequiredMixin, DeleteView):
    model = Pupil
    template_name = "delete.html"
    pk_url_kwarg = "pk"
    success_url = reverse_lazy("pupils")

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser and self.request.user != self.get_object().group.teacher:
            raise Http404("Not found")
        return super(PupilDelete, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "O'quvchi o'chirildi")
        return super(PupilDelete, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PupilDelete, self).get_context_data(**kwargs)
        context["title"] = self.object.full_name
        return context


@login_required(login_url="signin")
def delete_teacher(request, pk):
    teacher = User.objects.get(id=pk)

    if request.method == "POST":
        teacher.delete()
        messages.success(request, "O'qituvchi o'chirildi")
        return redirect("teachers")

    context = {
        "title": teacher.full_name,
    }
    return render(request, "delete.html", context)


class GroupDelete(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = "delete.html"
    success_url = reverse_lazy("groups")
    pk_url_kwarg = "pk"

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser and self.request.user != self.get_object().teacher:
            raise Http404("Not found")
        return super(GroupDelete, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "O'quvchi o'chirildi")
        return super(GroupDelete, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GroupDelete, self).get_context_data(**kwargs)
        context.update({
            "title": self.object.name,
            "btn_disabled": self.object.has_students,
            "btn_disabled_warning_text": "Guruhda o'quvchilar mavjud, avval o'quvchilarni barchasini o'chiring yoki boshqa guruhga o'tkazing",
        })
        return context


@login_required(login_url="signin")
def delete_subject(request, pk):
    subject = Subject.objects.get(id=pk)

    if request.method == "POST":
        subject.delete()
        messages.success(request, "Fan o'chirildi")
        return redirect("subjects")

    context = {
        "title": subject.name,
        "btn_disabled": subject.has_groups,
        "btn_disabled_warning_text": "Bu fanga bog'liq guruhlar mavjud. Shu guruhlarni o'chirib qaytadan urinib ko'ring",
    }
    return render(request, "delete.html", context)


class ExpenseDelete(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = "delete.html"
    success_url = reverse_lazy("expenses")
    pk_url_kwarg = "expense_id"

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser and self.request.user != self.get_object().owner:
            raise Http404("Not found")
        return super(ExpenseDelete, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Chiqim o'chirildi")
        return super(ExpenseDelete, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ExpenseDelete, self).get_context_data(**kwargs)
        context.update({
            "title": f'"{self.object.name}"',
        })
        return context
