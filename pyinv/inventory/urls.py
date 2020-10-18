from django.urls import path

from .views import (
    asset,
    consumable,
    consumable_model,
    misc,
    manufacturer,
    model,
)

app_name = "inventory"

urlpatterns = [
    path("", misc.SearchView.as_view(), name="index"),
    path("assets", asset.AssetSearchView.as_view(), name="asset_search"),
    path("assets/create", asset.AssetCreateView.as_view(), name="asset_create"),
    path("assets/<slug:slug>", asset.AssetDisplayView.as_view(), name="asset_view"),
    path(
        "assets/<slug:slug>/edit",
        asset.AssetUpdateView.as_view(),
        name="asset_edit",
    ),
    path(
        "assets/<slug:slug>/delete",
        asset.AssetDeleteView.as_view(),
        name="asset_delete",
    ),
    path(
        "consumablemodels/create",
        consumable_model.ConsumableModelCreateView.as_view(),
        name="consumablemodel_create",
    ),
    path(
        "consumablemodels/<int:pk>",
        consumable_model.ConsumableModelDisplayView.as_view(),
        name="consumablemodel_view",
    ),
    path(
        "consumablemodels/<int:pk>/edit",
        consumable_model.ConsumableModelUpdateView.as_view(),
        name="consumablemodel_edit",
    ),
    path(
        "consumablemodels/<int:pk>/delete",
        consumable_model.ConsumableModelDeleteView.as_view(),
        name="consumablemodel_delete",
    ),
    path("consumables", consumable.ConsumableSearchView.as_view(), name="consumable_search"),
    path(
        "consumables/create",
        consumable.ConsumableCreateView.as_view(),
        name="consumable_create",
    ),
    path(
        "consumables/<int:pk>/edit",
        consumable.ConsumableUpdateView.as_view(),
        name="consumable_edit",
    ),
    path("models", model.AssetModelSearchView.as_view(), name="model_search"),
    path(
        "models/<int:pk>",
        model.AssetModelDisplayView.as_view(),
        name="model_view",
    ),
    path("models/create", model.AssetModelCreateView.as_view(), name="model_create"),
    path(
        "models/<int:pk>/edit",
        model.AssetModelUpdateView.as_view(),
        name="model_edit",
    ),
    path(
        "models/<int:pk>/delete",
        model.AssetModelDeleteView.as_view(),
        name="model_delete",
    ),
    path("manufacturers", manufacturer.AssetManufacturerSearchView.as_view(), name="manufacturer_search"),
    path(
        "manufacturers/<int:pk>",
        manufacturer.AssetManufacturerDisplayView.as_view(),
        name="manufacturer_view",
    ),
    path(
        "manufacturers/create",
        manufacturer.AssetManufacturerCreateView.as_view(),
        name="manufacturer_create",
    ),
    path(
        "manufacturers/<int:pk>/edit",
        manufacturer.AssetManufacturerUpdateView.as_view(),
        name="manufacturer_edit",
    ),
    path(
        "manufacturers/<int:pk>/delete",
        manufacturer.AssetManufacturerDeleteView.as_view(),
        name="manufacturer_delete",
    ),
]
