from django.urls import path
from . import views
from a_financial_management.views import financial
urlpatterns = [
    path('login/', views.login_view, name='login_url'),
    path('register/', views.register, name='register_url'),
    path('logout/', views.logout_command, name='logout_url'),
    path('my-degrees/', views.my_degrees, name='my_degrees_url'),
    path('my-financial/', financial, name='my_financial_url'),


]