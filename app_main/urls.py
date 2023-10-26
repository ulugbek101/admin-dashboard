from django.urls import path

from . import views

urlpatterns = [
    path('subjects/', views.subjects, name='subjects'),
    path('groups/', views.groups, name='groups'),
    path('teachers/', views.teachers, name='teachers'),
    path('pupils/', views.pupils, name='pupils'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings, name='settings'),

    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('add-pupil/', views.add_pupil, name='add_pupil'),
]
