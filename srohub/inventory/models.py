from django.db import models


class AssetManufacturer(models.Model):
    """The manufacturer of an asset."""

    name = models.CharField(max_length=30)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AssetModel(models.Model):
    """The model of an asset."""

    name = models.CharField(max_length=30)
    is_container = models.BooleanField(default=False, verbose_name="Can contain assets")
    asset_manufacturer = models.ForeignKey(AssetManufacturer, on_delete=models.PROTECT)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Asset(models.Model):
    """An individual instance of a assetmodel."""

    class Condition(models.TextChoices):
        """The condition of an item."""
        UNKNOWN = 'U'
        BROKEN = 'B'
        NEEDS_ASSEMBLY = 'A'
        NEEDS_REPAIR = 'R'
        WORKING = 'W'

    asset_code = models.CharField(max_length=11)  # TODO: Validate
    name = models.CharField(max_length=30, null=True, blank=True)
    location = models.ForeignKey('Asset', on_delete=models.PROTECT)
    asset_model = models.ForeignKey(AssetModel, on_delete=models.PROTECT)
    condition = models.CharField(
        max_length=2,
        choices=Condition.choices,
        default=Condition.UNKNOWN,
    )
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)