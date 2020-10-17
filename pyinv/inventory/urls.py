from django.urls import path

from .views import (
    asset,
    consumable,
    consumable_model,
    index,
    manufacturer,
    model,
)

app_name = "inventory"

urlpatterns = [
    path("", index, name="index"),
    path("asset/search", asset.AssetSearchView.as_view(), name="asset_search"),
    path("asset/create", asset.AssetCreateView.as_view(), name="asset_create"),
    path("asset/<slug:slug>", asset.AssetDisplayView.as_view(), name="asset_view"),
    path(
        "asset/<slug:slug>/edit",
        asset.AssetUpdateView.as_view(),
        name="asset_edit",
    ),
    path(
        "asset/<slug:slug>/delete",
        asset.AssetDeleteView.as_view(),
        name="asset_delete",
    ),
    path(
        "consumablemodel/create",
        consumable_model.ConsumableModelCreateView.as_view(),
        name="consumablemodel_create",
    ),
    path(
        "consumablemodel/<int:pk>",
        consumable_model.ConsumableModelDisplayView.as_view(),
        name="consumablemodel_view",
    ),
    path(
        "consumablemodel/<int:pk>/edit",
        consumable_model.ConsumableModelUpdateView.as_view(),
        name="consumablemodel_edit",
    ),
    path(
        "consumablemodel/<int:pk>/delete",
        consumable_model.ConsumableModelDeleteView.as_view(),
        name="consumablemodel_delete",
    ),
    path(
        "consumable/<int:pk>/edit",
        consumable.ConsumableUpdateView.as_view(),
        name="consumable_edit",
    ),
    path(
        "model/<int:pk>",
        model.AssetModelDisplayView.as_view(),
        name="model_view",
    ),
    path("model/create", model.AssetModelCreateView.as_view(), name="model_create"),
    path(
        "model/<int:pk>/edit",
        model.AssetModelUpdateView.as_view(),
        name="model_edit",
    ),
    path(
        "model/<int:pk>/delete",
        model.AssetModelDeleteView.as_view(),
        name="model_delete",
    ),
    path(
        "manufacturer/<int:pk>",
        manufacturer.AssetManufacturerDisplayView.as_view(),
        name="manufacturer_view",
    ),
    path(
        "manufacturer/create",
        manufacturer.AssetManufacturerCreateView.as_view(),
        name="manufacturer_create",
    ),
    path(
        "manufacturer/<int:pk>/edit",
        manufacturer.AssetManufacturerUpdateView.as_view(),
        name="manufacturer_edit",
    ),
    path(
        "manufacturer/<int:pk>/delete",
        manufacturer.AssetManufacturerDeleteView.as_view(),
        name="manufacturer_delete",
    ),
]
