from django.urls import path
from . import views

urlpatterns = [
    path('courses-page/', views.courses, name='courses_url'),
    path('courses-detail/<int:pk>/', views.course_detail, name='course_detail_url'),

]