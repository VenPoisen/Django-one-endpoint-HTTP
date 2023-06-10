from django.urls import path
from . import views


urlpatterns = [
    path("", views.get_response_time, name="get_response_time")
]
