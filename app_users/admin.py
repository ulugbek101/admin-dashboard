from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from app_main.models import Expense
from .models import SMSSentCount

User = get_user_model()

admin.site.unregister(Group)
admin.site.register(Expense)
admin.site.register(SMSSentCount)


@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email']
