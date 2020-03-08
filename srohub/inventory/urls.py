from django.urls import path

from . import views

app_name = "inventory"

urlpatterns = [
    path('', views.InventorySearchView.as_view(), name='index'),
    path('asset/<slug:slug>', views.AssetDisplayView.as_view(), name='asset_view'),
    path('asset/<slug:slug>/edit', views.AssetUpdateView.as_view(), name='asset_edit'),
    path('model/<int:pk>', views.AssetModelDisplayView.as_view(), name='model_view'),
    path('manufacturer/<int:pk>', views.AssetManufacturerDisplayView.as_view(), name='manufacturer_view'),
]
