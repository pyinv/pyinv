from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import (
    Asset,
    AssetManufacturer,
    AssetModel,
    Consumable,
    ConsumableModel,
)


class AssetAdmin(SimpleHistoryAdmin):
    raw_id_fields = ["location", "asset_model"]
    list_display = [
        "display_name",
        "asset_code",
        "asset_model",
        "condition",
        "location",
    ]
    list_filter = ["condition"]
    history_list_display = ["condition", "location__name"]
    search_fields = [
        "asset_code",
        "name",
        "notes",
        "asset_model__name",
        "asset_model__asset_manufacturer__name",
    ]


class AssetModelAdmin(SimpleHistoryAdmin):
    list_display = ["name", "asset_manufacturer", "is_container"]
    list_filter = ["is_container"]
    history_list_display = list_display + ["notes"]
    search_fields = ["name", "asset_manufacturer__name", "notes"]


class AssetManufacturerAdmin(SimpleHistoryAdmin):
    list_display = ["name"]
    search_fields = ["name"]


class ConsumableModelAdmin(SimpleHistoryAdmin):
    list_display = ["name", "asset_manufacturer"]
    search_fields = ["name", "asset_manufacturer__name", "notes"]


class ConsumableAdmin(SimpleHistoryAdmin):
    raw_id_fields = ["location", "consumable_model"]
    list_display = ["consumable_model", "quantity", "location"]
    search_fields = [
        "consumable_model__name",
        "consumable_model__asset_manufacturer__name",
        "notes",
    ]


admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetModel, AssetModelAdmin)
admin.site.register(AssetManufacturer, AssetManufacturerAdmin)
admin.site.register(ConsumableModel, ConsumableModelAdmin)
admin.site.register(Consumable, ConsumableAdmin)
