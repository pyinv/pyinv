from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("signup", views.SignUp.as_view(), name="signup"),
    path("profile", views.Profile.as_view(), name="profile"),
    path("preferences", views.Preferences.as_view(), name="preferences"),
]
