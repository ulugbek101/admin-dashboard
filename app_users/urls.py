from django.urls import path, include

from . import views


urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),

    path('send-sms/', views.send_sms, name='send_sms'),
    
    path('teacher/<uuid:id>/', views.TeacherDetail.as_view(), name='teacher_detail'),
]
