from django.contrib import admin

from .models import AssetManufacturer, AssetModel, Asset

admin.site.register(Asset)
admin.site.register(AssetModel)
admin.site.register(AssetManufacturer)
