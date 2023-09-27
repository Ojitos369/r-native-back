from django.urls import path

from .api import (
    CreateUser
)

app_name = "api_users"
urlpatterns = [
    path("create_user/", CreateUser.as_view(), name=f"{app_name}_create_user"),
]