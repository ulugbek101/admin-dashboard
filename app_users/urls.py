from django.urls import path, include

from . import views


urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.CustomLogoutView.as_view(), name='signout'),

    # path('social-auth/', include('social_django.urls', namespace='social')),
]
