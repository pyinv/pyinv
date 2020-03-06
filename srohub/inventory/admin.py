from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import AssetManufacturer, AssetModel, Asset


class AssetHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["display_name", "asset_code", "asset_model", "condition", "location"]
    history_list_display = ["condition", "location"]
    search_fields = ['name', 'notes', "location"]


admin.site.register(Asset, AssetHistoryAdmin)
admin.site.register(AssetModel, SimpleHistoryAdmin)
admin.site.register(AssetManufacturer, SimpleHistoryAdmin)
