from datetime import date

from django.db.models import Sum, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, CreateView

import pandas as pd

from app_users.models import User
from . import forms
from . import utils

from .decorators import is_superuser
from .models import Group, Pupil, Payment, Subject, Expense
from utils.mixins import IsSuperuserOrAdminMixin
from utils.sms_texts import sms_texts


class SubjectList(LoginRequiredMixin, ListView):
    """Return subjects list"""
    template_name = "app_main/subjects.html"
    context_object_name = "subjects_list"
    extra_context = {
        "title": "Fanlar",
        "subjects": True
    }

    def get_queryset(self):
        """
        Return subjects list if user is superuser,
        otherwise throw 404 error
        """
        subjects = Subject.objects.annotate(pupils=Count("group__pupil"))
        if not self.request.user.is_superuser and not self.request.user.is_admin:
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
        if self.request.user.is_superuser or self.request.user.is_admin:
            return Group.objects.all()
        return Group.objects.filter(teacher=self.request.user).order_by("name", "-created")


class GroupDetail(LoginRequiredMixin, DetailView):
    model = Group
    template_name = "app_main/group_detail.html"
    pk_url_kwarg = "id"
    context_object_name = "group"

    def dispatch(self, request, *args, **kwargs):
        if (not self.request.user.is_superuser and not self.request.user.is_admin) and self.request.user != self.get_object().teacher:
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
        "pupils": True,
        "sms_texts": sms_texts,
    }
    paginator_class = Paginator
    paginate_by = 50
    page_kwarg = 'page'

    def get_queryset(self):
        """
        Return all students if user is superuser,
        otherwise only students of the teacher
        """

        if self.request.GET.get('search-field'):
            q = self.request.GET.get('search-field')
            pupils = Pupil.objects.filter(Q(first_name__icontains=q) | Q(
                last_name__icontains=q) | Q(phone_number__icontains=q))
        else:
            pupils = Pupil.objects.all().order_by(
                "first_name", "last_name", "group", "-created"
            )

        if not self.request.user.is_superuser and not self.request.user.is_admin:
            return pupils.filter(group__teacher=self.request.user)
        return pupils

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context['page_obj']

        left_index = page_obj.number - 2
        right_index = page_obj.number + 2

        if left_index - 2 < 1:
            left_index = 1
            right_index = left_index + 4

        if right_index > page_obj.paginator.num_pages:
            right_index = page_obj.paginator.num_pages
            left_index = 1
            if right_index - 4 > 0:
                left_index = right_index - 4

        context['searchField'] = self.request.GET.get(
            'search-field') if self.request.GET.get('search-field') else ""
        context['page_range'] = range(left_index, right_index + 1)
        return context


class ExpenseListByTeacher(LoginRequiredMixin, IsSuperuserOrAdminMixin, ListView):
    """ Render expenses list for specific teacher """
    template_name = "app_main/expenses_by_teacher.html"
    context_object_name = "expenses_list"
    extra_context = {
        "title": "Chiqimlar ro'yxati",
        "expenses": True
    }

    def get_queryset(self):
        """
        Return all expenses of a specific teacher for this month
        """
        expenses = Expense.objects.filter(owner__id=self.kwargs['teacher_id'], created__year=date.today(
        ).year, created__month=date.today().month).order_by("-created")
        return expenses


class ExpenseList(LoginRequiredMixin, ListView):
    """ Render expenses list """

    template_name = "app_main/expenses.html"
    context_object_name = "expenses_list"
    extra_context = {
        "title": "Chiqimlar ro'yxati",
        "title_for_superuser": "Chiqim olganlar ro'yxati",
        "expenses": True
    }

    def get_queryset(self):
        """
        Return all expenses if user is superuser,
        otherwise only expenses of the user
        """

        expenses = Expense.objects.filter(created__year=date.today().year, created__month=date.today().month).order_by(
            "-created")
        if not self.request.user.is_superuser:
            return expenses.filter(owner=self.request.user)
        return expenses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers_with_expenses'] = User.objects.annotate(
            total_expenses_amount=Sum(
                'expense__amount',
                filter=Q(expense__created__month=date.today().month,
                         expense__created__year=date.today().year)
            ),
            total_expenses_count=Count(
                'expense',
                filter=Q(expense__created__month=date.today().month,
                         expense__created__year=date.today().year)
            )
        ).filter(total_expenses_amount__gt=0).order_by('first_name', '-created')
        return context


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

        if (not self.request.user.is_superuser and not request.user.is_admin) and self.get_object().owner != self.request.user:
            raise Http404("Not found")
        return super(ExpenseDetail, self).dispatch(request, *args, **kwargs)


@login_required(login_url="signin")
@is_superuser
def dashboard(request):
    groups = Group.objects.all()
    total_paid, total_payment = utils.get_payment_info(
        year=date.today().year, month=date.today().month
    )

    payments = Payment.objects.filter(
        month__lte=date.today()).order_by("created")

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
@is_superuser
def download_stats(request):
    # Getting months list
    months = utils.get_months()

    # Identifying current year
    year = date.today().year

    # Identifying month selected by user, current or previous
    month = request.POST.get("month")
    if month == "current":
        month = date.today().month
    else:
        month = date.today().month - 1
        if month < 1:
            year -= 1
            month = 12

    payments_dataset_by_groups, groups = utils.get_total_payment_info_by_groups(
        year=year, month=month)
    expenses_dataset, expenses = utils.get_expenses_amount(
        year=year, month=month)
    overall_expenses_amount = utils.get_total_expenses_amount(
        year=year, month=month)
    # total_paid, total_payment = utils.get_payment_info(year=year, month=month)

    # Creating Excel file
    writer = pd.ExcelWriter("stats.xlsx", engine="openpyxl")

    teachers = User.objects.all()
    for teacher in teachers:

        # Skip the teacher with no groups
        teacher_groups = Group.objects.filter(teacher=teacher)
        teacher_pupils = Pupil.objects.filter(group__in=teacher_groups)

        if teacher_pupils.count() == 0:
            continue

        data = {
            "№": [],
            "Guruh": [],
            "O'quvchi": [],
            "Oy": [],
            "To'lov (so'm)": [],
            "Qo'shimcha ma'lumot": [],
        }

        for group in teacher.group_set.filter(Q(created__month__lte=month, created__year__lte=year) | Q(created__month__lte=month)):

            # Skip group if there is no pupil
            if group.pupil_set.count() == 0:
                continue

            for index, pupil in enumerate(group.pupil_set.filter(created__year=year, created__month__lte=month), 1):
                pupil_payment = pupil.payment_set.filter(
                    month__year=year, month__month=month).first()

                if pupil_payment:
                    group_name = pupil_payment.group.name if pupil_payment.group else pupil_payment.group_name
                    pupil_name = pupil_payment.pupil.full_name if pupil_payment.pupil else pupil_payment.pupil_fullname
                    month_name = months[month]
                    amount = f"{utils.format_number(pupil_payment.amount)} / {utils.format_number(group.price)}"
                    note = pupil_payment.note if pupil_payment.note else "-"
                else:
                    group_name = group.name
                    pupil_name = pupil.full_name
                    month_name = months[month]
                    amount = f"{0} / {utils.format_number(group.price)}"
                    note = "-"

                data["№"].append(index)
                data["Guruh"].append(group_name)
                data["O'quvchi"].append(pupil_name)
                data["Oy"].append(month_name)
                data["To'lov (so'm)"].append(amount)
                data["Qo'shimcha ma'lumot"].append(note)

            group_payment_total = group.price * group.pupil_set.count()
            group_payment_paid = Payment.objects.filter(month__year=year, month__month=month, group=group).aggregate(
                total_paid=Sum("amount")).get("total_paid")

            data["№"].append("")
            data["Guruh"].append("")
            data["O'quvchi"].append("")
            data["Oy"].append("")
            data["To'lov (so'm)"].append(
                f"{group_payment_paid or 0} / {group_payment_total}")
            data["Qo'shimcha ma'lumot"].append("")

            # Add 2 new lines between groups
            data = {key: value + [''] for key, value in data.items()}
            data = {key: value + [''] for key, value in data.items()}
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name=teacher.full_name, index=False)

    # ======================== Adding groups dataframe to an Excel document as a separate sheet ========================
    # Creating special variables to insert them to the end of row for payments column in an Excel sheet
    total_paid_by_groups = sum([group.get("total_paid")
                               for group in payments_dataset_by_groups])
    total_payment_by_groups = sum(
        [group.get("total_payment") for group in payments_dataset_by_groups])

    groups_dataset = {
        "Guruh": [group.get("name") for group in payments_dataset_by_groups] + ["-",
                                                                                "-"],
        "To'langan": [group.get("total_paid") for group in payments_dataset_by_groups] +
                     ["-", total_paid_by_groups],
        "Kutilayotgan tushum": [group.get("total_payment") for group in payments_dataset_by_groups] +
                               ["-", total_payment_by_groups],
    }
    df = pd.DataFrame(groups_dataset)
    df.index = df.index + 1
    df.to_excel(
        writer, sheet_name="Guruhlar bo'yicha tushumlar", index_label="\u2116")
    # ==================================================================================================================
    # ======================= Adding expenses dataframe to an Excel document as a separate sheet =======================
    expenses_dataset = {
        "Chiqim nomi": [expense.get("name") for expense in expenses_dataset],
        "O'qituvchi": [expense.get("owner") for expense in expenses_dataset],
        "Miqdor": [utils.format_number(expense.get("amount")) for expense in expenses_dataset],
        "Qo'shimcha ma'lumot": [expense.get("note") for expense in expenses_dataset],
        "Olingan sana": [expense.get("date") for expense in expenses_dataset],
    }
    df = pd.DataFrame(expenses_dataset)
    df.index = df.index + 1
    df.to_excel(writer, sheet_name="Chiqimlar", index_label="\u2116")
    # ==================================================================================================================
    # ======================= Adding overall dataframe to an Excel document as a separate sheet ========================
    overall_stats_dataframe = {
        "Tushum": [total_paid_by_groups],
        "Chiqim": [utils.format_number(overall_expenses_amount) or 0],
        "Foyda": [utils.format_number((total_paid_by_groups or 0) - (overall_expenses_amount or 0))],
    }
    df = pd.DataFrame(overall_stats_dataframe)
    df.to_excel(writer, sheet_name="Umumiy statistika", index=False)
    # ==================================================================================================================

    writer.close()

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename={months[month]}-{year} statistikasi.xlsx'

    with open("stats.xlsx", "rb") as excel_file:
        response.write(excel_file.read())

    return response


@login_required(login_url='signin')
@is_superuser
def download_stats_page(request):
    context = {
        'download_stats': True,
    }
    return render(request, 'app_main/download_stats_page.html', context)


@login_required(login_url="signin")
def settings(request):
    if request.method == "POST":
        password1, password2, first_name, last_name, email, profile_picture, job = (
            request.POST.get("password1"),
            request.POST.get("password2"),
            request.POST.get("first_name"),
            request.POST.get("last_name"),
            request.POST.get("email"),
            request.FILES.get("profile_picture"),
            request.POST.get("job"),
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
        "btn_text": "Profil ma'lumotlarini yangilash",
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
        if not self.request.user.is_superuser and not self.request.user.is_admin:
            raise Http404("Not found")
        return super(TeacherCreate, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TeacherCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass request.user to the form
        return kwargs

    def form_valid(self, form):
        password1 = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")

        if password1 == password2:
            teacher = form.save(commit=False)

            if form.cleaned_data.get('job'):
                # Set user status if provided
                teacher.job = form.cleaned_data.get('job')

                # Set user privileges based on status
                if form.cleaned_data.get("job") == "superuser":
                    teacher.is_superuser = True
                    teacher.is_admin = True

                elif form.cleaned_data.get("job") == "admin":
                    teacher.is_superuser = False
                    teacher.is_admin = True

                elif form.cleaned_data.get("job") == "teacher":
                    teacher.is_superuser = False
                    teacher.is_admin = False

            teacher.username = self.request.POST.get("email")[
                : self.request.POST.get("email").find("@")
            ]

            if password1 and password2:
                # Set password if password is provided
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
        if self.request.user != group.teacher and (not self.request.user.is_superuser and not self.request.user.is_admin):
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

    if not request.user.is_superuser and not request.user.is_admin and request.user != pupil.group.teacher:
        messages.error(
            request, "Boshqalarning o'quvchisini uchun to'lov qila olmaysiz")
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
                "note": payment.note if payment.note else "",
            }
        )

        if payment:
            form.data['amount'] = payment.amount

    # Otherwise display a form with blank note field
    else:
        form = forms.PaymentForm(data={})

        if payment:
            form.data['amount'] = payment.amount

    pupil = Pupil.objects.get(group__id=group_id, id=pupil_id)

    if request.method == "POST":
        if payment:
            form = forms.PaymentForm(request.POST, instance=payment)
        else:
            form = forms.PaymentForm(request.POST)

        if form.is_valid():
            if request.POST.get("amount") == "0":
                messages.error(
                    request, "To'lov miqdori 0 bo'lishi mumkin emas")
                return redirect("add_payment", group_id=group_id, pupil_id=pupil_id)

            if int(request.POST.get("amount")) > pupil.group.price:
                messages.error(
                    request, "To'lov miqdori guruh to'lovi moiqdoridan ko'p")
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
            messages.error(
                request, "Guruh to'lovi miqdori 0 bo'lishi mumkin emas")
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
    extra_context = {
        "title": "Guruh qo'shish",
        "btn_text": "Guruhni qo'shish",
    }

    def get_success_url(self):
        return reverse("group_detail", kwargs={"pk": self.get_object().id})

    def form_valid(self, form):
        messages.success(self.request, "Guruh yaratildi")
        return super(GroupCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Guruh to'lovi miqdori 0 bo'lishi mumkin emas")
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

        if not self.request.user.is_superuser and not self.request.user.is_admin:
            raise Http404("Not found")
        return super(SubjectCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Fan qo'shildi")
        return super(SubjectCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Bunday fan allaqachon mavjud yoki Fan nomi juda qisqa")
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if self.request.method == 'POST':
            form = self.form_class(request.POST, request.FILES)

            if self.request.user.is_superuser:
                form.owner = request.POST.get('owner')
            else:
                form.owner = request.user

            if form.is_valid():
                form.save()
                return redirect("expenses")

        return super(ExpenseCreate, self).dispatch(request, *args, **kwargs)

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

    extra_context = {
        "title": "O'quvchi ma'lumotlarini o'zgartirish",
        "btn_text": "O'quvchi ma'lumotlarini yangilash",
    }

    def get_success_url(self):
        return reverse("group_detail", kwargs={"id": self.get_object().group.id})

    def dispatch(self, request, *args, **kwargs):
        if (not self.request.user.is_superuser and not self.request.user.is_admin) and self.request.user != self.get_object().group.teacher:
            raise Http404("Not found")
        return super(PupilUpdate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "O'quvchi ma'lumotlari yangilandi")
        return super(PupilUpdate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Forma noto'g'ri to'ldirilgan. Bundan ma'lumotlarga ega o'quvchi mavjud")
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
        if (not self.request.user.is_superuser and not request.user.is_admin) and self.request.user != self.get_object():
            raise Http404("Not found")
        return super(TeacherUpdate, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TeacherUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass request.user to the form
        kwargs['update_form'] = True
        return kwargs

    def form_valid(self, form):
        password1 = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")
        teacher = self.object

        if form.cleaned_data.get("job"):
            teacher.job = form.cleaned_data.get("job")

            # Set user privileges based on status
            if form.cleaned_data.get("job") == "superuser":
                teacher.is_superuser = True
                teacher.is_admin = True

            elif form.cleaned_data.get("job") == "admin":
                teacher.is_superuser = False
                teacher.is_admin = True

            elif form.cleaned_data.get("job") == "teacher":
                teacher.is_superuser = False
                teacher.is_admin = False

        if password1 or password2:
            if password1 == password2:
                teacher.set_password(password2)

            else:
                messages.error(self.request, "Parollar bir xil bo'lishi shart")
                return redirect("update_teacher", pk=teacher.id)

        teacher.save()
        messages.success(
            self.request, "O'qituvchi ma'lumotlari yangilandi")
        return redirect("teachers")

    def form_invalid(self, form):
        messages.error(
            self.request, "O'qituvchi ism va familiyaga ega bo'lishi shart")
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
            messages.success(request, "Fan yangilandi")
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

    def dispatch(self, request, *args, **kwargs):
        if (not self.request.user.is_superuser and not self.request.user.is_admin) and self.request.user != self.get_object().group.teacher:
            raise Http404("Not found")
        return super(PupilDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse("group_detail", kwargs={"id": self.get_object().group.id})

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
        "btn_disabled": teacher.group_set.all().count() != 0,
        "btn_disabled_warning_text": "O'qituvchiga bog'langan guruhlar mvjud, avval guruhlarni o'chiring keyin o'qituvchini o'chirishingiz mumkin bo'ladi",
    }
    return render(request, "delete.html", context)


class GroupDelete(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = "delete.html"
    success_url = reverse_lazy("groups")
    pk_url_kwarg = "pk"

    def dispatch(self, request, *args, **kwargs):
        if (not self.request.user.is_superuser and not self.request.user.is_admin) and self.request.user != self.get_object().teacher:
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
        # and self.request.user != self.get_object().owner:
        if not self.request.user.is_superuser and not self.request.user.is_admin:
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


class PaymentsList(LoginRequiredMixin, IsSuperuserOrAdminMixin, ListView):
    model = Payment
    template_name = 'app_main/payments.html'
    context_object_name = 'payments_list'
    ordering = ['created', 'pupil']
    extra_context = {
        'current_date': date.today().strftime("%Y-%m-%d"),
        'payments': True,
    }
    paginate_by = 100
    paginator_class = Paginator
    page_kwarg = 'page'

    def get(self, request):
        if request.GET.get('date'):
            year, month, day = request.GET.get('date').split('-')
            self.queryset = Payment.objects.filter(
                updated__year=year, updated__month=month, updated__day=day)
            self.extra_context['current_date'] = request.GET.get('date')
            self.extra_context['title'] = f"{request.GET.get('date')} dagi to'lovlar"

            return super().get(request)
        else:
            self.queryset = Payment.objects.filter(updated__year=date.today(
            ).year, updated__month=date.today().month, updated__day=date.today().day)
            self.extra_context['current_date'] = date.today().strftime(
                "%Y-%m-%d")
            self.extra_context['title'] = f"Bugugi to'lovlar"
            return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context['page_obj']

        left_index = page_obj.number - 2
        right_index = page_obj.number + 2

        if left_index - 2 < 1:
            left_index = 1
            right_index = left_index + 4

        if right_index > page_obj.paginator.num_pages:
            right_index = page_obj.paginator.num_pages
            left_index = 1
            if right_index - 4 > 0:
                left_index = right_index - 4

        context['page_range'] = range(left_index, right_index + 1)
        return context
