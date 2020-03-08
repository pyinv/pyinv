from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import AssetManufacturer, AssetModel, Asset


class AssetAdmin(SimpleHistoryAdmin):
    raw_id_fields = ["location"]
    readonly_fields = ["asset_code"]
    list_display = ["display_name", "asset_code", "asset_model", "condition", "location"]
    list_filter = ["condition"]
    history_list_display = ["condition", "location"]
    search_fields = ['asset_code', 'name', 'notes', "asset_model__name", "asset_model__asset_manufacturer__name"]


class AssetModelAdmin(SimpleHistoryAdmin):
    list_display = ["name", "asset_manufacturer", "is_container"]
    list_filter = ["is_container"]
    history_list_display = list_display + ["notes"]
    search_fields = ["name", "asset_manufacturer__name", "notes"]


class AssetManufacturerAdmin(SimpleHistoryAdmin):
    list_display = ["name"]
    search_fields = ["name"]


admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetModel, AssetModelAdmin)
admin.site.register(AssetManufacturer, AssetManufacturerAdmin)
