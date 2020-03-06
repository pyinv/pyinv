from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = "inventory"

urlpatterns = [
    path('', login_required(views.InventorySearchView.as_view()), name='index'),
    path('asset/<slug:slug>', login_required(views.AssetDisplayView.as_view()), name='asset_view'),
    path('model/<int:pk>', login_required(views.AssetModelDisplayView.as_view()), name='model_view'),
]
