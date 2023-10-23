from django import forms
from app_users.models import User
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _


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
        widgets = {
            "first_name": forms.TextInput(attrs={
                "placeholder": "Ism",
            }),
            "last_name": forms.TextInput(attrs={
                "placeholder": "Familiya",
            }),
            "email": forms.TextInput(attrs={
                "placeholder": "E-mail manzil",
            }),
        }