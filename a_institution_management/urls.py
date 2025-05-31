from django.urls import path
from . import views
urlpatterns = [
    path("set-dropdown/", views.set_dropdown_value, name="set_dropdown_value"),
    # ... other admin/urls
]