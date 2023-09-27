from django.urls import path

from apis.api import (
    Test
)

urlpatterns = [
    path('test/', Test.as_view(), name='test'),
]