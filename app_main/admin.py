from django.contrib import admin

from .models import Subject, Group, Pupil, Payment
from app_users.models import User

admin.site.unregister(User)
admin.site.register(Subject)
admin.site.register(Group)
admin.site.register(Pupil)
admin.site.register(Payment)

@admin.register(User)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name']
    list_display_links = ['email']
