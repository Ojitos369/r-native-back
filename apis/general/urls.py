from django.urls import path

from .api import (
    Version
)

app_name = "api_general"
urlpatterns = [
    path("version/", Version.as_view(), name=f"{app_name}_version"),
]