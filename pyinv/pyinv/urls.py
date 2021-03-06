"""srohub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path

admin.site.site_title = "PyInv Admin"
admin.site.site_header = "PyInv Admin"
admin.site.index_title = "PyInv Admin"

urlpatterns = [
    path("", include("inventory.urls", namespace="inventory")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("admin/", admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),
    path("oobe/", include("oobe.urls", namespace="oobe")),
]


def handler403(request, exception, template_name="403.html"):
    return render(request, template_name, {}, status=403)


def handler404(request, exception, template_name="404.html"):
    return render(request, template_name, {}, status=404)
