from django.urls import path

from . import views

app_name = "inventory"

urlpatterns = [
    path('', views.InventorySearchView.as_view(), name='index'),
    path('asset/<slug:slug>', views.AssetDisplayView.as_view(), name='asset_view'),
    path('asset/<slug:slug>/edit', views.AssetUpdateView.as_view(), name='asset_edit'),
    path('asset/<slug:slug>/delete', views.AssetDeleteView.as_view(), name='asset_delete'),
    path('consumablemodel/<int:pk>', views.ConsumableModelDisplayView.as_view(), name='consumablemodel_view'),
    path('consumablemodel/<int:pk>/edit', views.ConsumableModelUpdateView.as_view(), name='consumablemodel_edit'),
    path('model/<int:pk>', views.AssetModelDisplayView.as_view(), name='model_view'),
    path('model/<int:pk>/edit', views.AssetModelUpdateView.as_view(), name='model_edit'),
    path('model/<int:pk>/delete', views.AssetModelDeleteView.as_view(), name='model_delete'),
    path('manufacturer/<int:pk>', views.AssetManufacturerDisplayView.as_view(), name='manufacturer_view'),
    path('manufacturer/<int:pk>/edit', views.AssetManufacturerUpdateView.as_view(), name='manufacturer_edit'),
    path('manufacturer/<int:pk>/delete', views.AssetManufacturerDeleteView.as_view(), name='manufacturer_delete'),
]
