from datetime import date

from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from app_users.models import User
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from .models import Pupil, Payment, Group


class TeacherForm(forms.ModelForm):
    # password1 = forms.CharField(
    #     label=_("Password"),
    #     strip=False,
    #     widget=forms.PasswordInput(attrs={
    #         "autocomplete": "new-password",
    #         "placeholder": "Parol",
    #     }),
    #     help_text=password_validation.password_validators_help_text_html(),
    # )
    # password2 = forms.CharField(
    #     label=_("Password confirmation"),
    #     widget=forms.PasswordInput(attrs={
    #         "autocomplete": "new-password",
    #         "placeholder": "Parolni tasdiqlang",
    #     }),
    #     strip=False,
    #     help_text=_("Enter the same password as before, for verification."),
    # )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email",
                  "profile_picture"]
        widgets = {
            "profile_picture": forms.FileInput(attrs={
                "accept": "image/*"
            })
        }


class PupilForm(forms.ModelForm):
    class Meta:
        model = Pupil
        fields = '__all__'


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['month', 'amount', 'note']
        widgets = {
            'month': forms.DateInput(attrs={
                "type": "date",
                "value": date.today(),
                "min": date.today(),
            }),
            'amount': forms.NumberInput(attrs={
                "step": 5000,
            })
        }



class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['subject', 'name', 'teacher', 'price']



