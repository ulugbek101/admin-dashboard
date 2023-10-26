from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from app_users.models import User
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from .models import Pupil

class TeacherForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "placeholder": "Parol",
            }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "placeholder": "Parolni tasdiqlang",
            }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "profile_picture", "password1", "password2"]
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for _, field in self.fields.items():
    #         field.widget.attrs.update({
    #             "placeholder": field.label,
    #         })
        


class PupilForm(forms.ModelForm):
    class Meta:
        model = Pupil
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for _, field in self.fields.items():
    #         field.widget.attrs.update({
    #             "placeholder": field.label,
    #         })