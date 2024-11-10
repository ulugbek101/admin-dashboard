from datetime import date

from django import forms
from django.contrib.auth import password_validation

from app_users.models import User
from django.utils.translation import gettext_lazy as _

from .models import Pupil, Payment, Group, Subject, Expense


class TeacherForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        update_form = kwargs.pop('update_form', None)
        updating_user = kwargs.get('instance')
        super(TeacherForm, self).__init__(*args, **kwargs)

        if updating_user:
            if (user.is_admin and not user.is_superuser) and (
                    (kwargs.get('instance').is_admin and not kwargs.get('instance').is_superuser) or
                    (not kwargs.get('instance').is_admin and not kwargs.get('instance').is_superuser)
            ):
                self.fields.pop('job')

        # if user.is_admin and not user.is_superuser:
        #     self.fields.pop('job')

        if update_form:
            # Allow update teachers' profile without changing their passwords
            self.fields.get('password1').required = False
            self.fields.get('password2').required = False

    password1 = forms.CharField(
        label=_("Parol"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Parolni takrorlang"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Parollar bir xil bo'lishi kerak"),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email",
                  "profile_picture", "job", "password1", "password2"]
        widgets = {
            "profile_picture": forms.FileInput(attrs={
                "accept": "image/*"
            }),
            "job": forms.Select()
        }


class PupilForm(forms.ModelForm):
    class Meta:
        model = Pupil
        fields = ['first_name', 'last_name', 'phone_number', 'is_preferential']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'autofocus': 'true',
            }),
            'phone_number': forms.TextInput(attrs={
                'type': 'tel',
                'id': 'phone',
                'placeholder': '(+998) 99-000-00-00',
                'value': '+998'
            }),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['month', 'amount', 'note']
        widgets = {
            'month': forms.DateInput(attrs={
                "type": "date",
                "min": date.today(),
                "readonly": "true",
                # "disabled": "true",
            }),
            'amount': forms.TextInput(attrs={
                "autofocus": "true",
            })
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['subject', 'name', 'teacher', 'price']


class GroupUpdateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["teacher", "subject", "name"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(GroupUpdateForm, self).__init__(*args, **kwargs)

        # Check if the user is not a superuser
        if user and not user.is_superuser:
            # Remove certain fields from the form
            del self.fields["teacher"]
            del self.fields["subject"]
            # Add more conditions and field removals as needed


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name"]


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['owner', 'name', 'amount', 'note']
        widgets = {
            'amount': forms.TextInput(attrs={
                "value": 0,
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ExpenseForm, self).__init__(*args, **kwargs)

        if user and not user.is_superuser and not user.is_admin:
            self.fields.pop('owner')
