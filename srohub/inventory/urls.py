from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = "inventory"

urlpatterns = [
    path('', login_required(views.InventorySearchView.as_view()), name='index'),
]
