from django.urls import path

from . import views

app_name = "oobe"

urlpatterns = [
    path("", views.OOBE.as_view(), name="index"),
]
