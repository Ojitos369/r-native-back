from django.urls import path

from .api import (
    Login
)

app_name = "api_login"
urlpatterns = [
    path("login/", Login.as_view(), name=f"{app_name}_login"),
]