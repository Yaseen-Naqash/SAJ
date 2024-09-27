from django.urls import path
from . import views

urlpatterns = [
    path('student-login/', views.students_login, name='student_login_url'),
    path('teacher-login/', views.teachers_login, name='teacher_login_url'),
    path('register/', views.register, name='register_url'),
    

]