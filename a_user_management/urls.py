from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.students_login, name='student_login_url'),
]