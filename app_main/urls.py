from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    path('subjects/', views.subjects, name='subjects'),
    path('groups/', views.groups, name='groups'),
    path('teachers/', views.teachers, name='teachers'),
    path('pupils/', views.pupils, name='pupils'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings, name='settings'),

    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('add-pupil/', views.add_pupil, name='add_pupil'),
    
    path('add-payment/<str:group_id>/<str:pupil_id>/', views.add_payment, name='add_payment'),
    
    path('update-pupil/<str:pk>/', views.update_pupil, name='update_pupil'),
    path('uptdate-teacher/<str:pk>/', views.update_teacher, name='update_teacher'),


    path('delete-pupil/<str:pk>/', views.delete_pupil, name='delete_pupil'),
    path('delete-teacher/<str:pk>/', views.update_teacher, name='delete_teacher'),
]
