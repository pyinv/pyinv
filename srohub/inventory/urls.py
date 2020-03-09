from django.urls import path

from . import views

app_name = "inventory"

urlpatterns = [
    path('', views.InventorySearchView.as_view(), name='index'),
    path('asset/<slug:slug>', views.AssetDisplayView.as_view(), name='asset_view'),
    path('asset/<slug:slug>/edit', views.AssetUpdateView.as_view(), name='asset_edit'),
    path('asset/<slug:slug>/delete', views.AssetDeleteView.as_view(), name='asset_delete'),
    path('model/<int:pk>', views.AssetModelDisplayView.as_view(), name='model_view'),
    path('model/<int:pk>/edit', views.AssetModelUpdateView.as_view(), name='model_edit'),
    path('manufacturer/<int:pk>', views.AssetManufacturerDisplayView.as_view(), name='manufacturer_view'),
    path('manufacturer/<int:pk>/edit', views.AssetManufacturerUpdateView.as_view(), name='manufacturer_edit'),
    path('manufacturer/<int:pk>/delete', views.AssetManufacturerDeleteView.as_view(), name='manufacturer_delete'),
]
