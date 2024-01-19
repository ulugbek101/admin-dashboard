from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('subjects/', views.SubjectList.as_view(), name='subjects'),

    path('groups/', views.GroupList.as_view(), name='groups'),
    path('group/<uuid:id>/', views.GroupDetail.as_view(), name='group_detail'),

    path('teachers/', views.TeacherList.as_view(), name='teachers'),
    path('pupils/', views.PupilList.as_view(), name='pupils'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings, name='settings'),
    path('expenses/', views.ExpenseList.as_view(), name='expenses'),

    path('add-teacher/', views.TeacherCreate.as_view(), name='add_teacher'),
    path('add-pupil/', views.PupilCreate.as_view(), name='add_pupil'),
    path('add-group/', views.add_group, name='add_group'),
    path('add-subject/', views.SubjectCreate.as_view(), name='add_subject'),
    path('add-payment/<uuid:group_id>/<uuid:pupil_id>/',
         views.add_payment, name='add_payment'),

    path('update-pupil/<uuid:pk>/', views.PupilUpdate.as_view(), name='update_pupil'),
    path('update-teacher/<uuid:pk>/', views.TeacherUpdate.as_view(), name='update_teacher'),
    path('update-group/<uuid:pk>/', views.update_group, name='update_group'),
    path('update-subject/<uuid:pk>/', views.update_subject, name='update_subject'),

    path('delete-pupil/<uuid:pk>/', views.PupilDelete.as_view(), name='delete_pupil'),
    path('delete-teacher/<uuid:pk>/', views.delete_teacher, name='delete_teacher'),
    path('delete-group/<uuid:pk>/', views.GroupDelete.as_view(), name='delete_group'),
    path('delete-subject/<uuid:pk>/', views.delete_subject, name='delete_subject'),

    path('download-stats/', views.download_stats, name='download_stats')
]
