from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login_url'),
    path('register/', views.register, name='register_url'),
    path('logout/', views.logout_command, name='logout_url'),
]