from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords

from .asset_code import generate_asset_code, validate_asset_code


class AssetManufacturer(models.Model):
    """The manufacturer of an asset."""

    name = models.CharField(max_length=30)
    notes = models.TextField(blank=True)
    history = HistoricalRecords()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("inventory:manufacturer_view", args=[self.pk])

    def get_edit_url(self):
        return reverse("inventory:manufacturer_edit", args=[self.pk])

    def get_delete_url(self):
        return reverse("inventory:manufacturer_delete", args=[self.pk])


class AssetModel(models.Model):
    """The model of an asset."""

    name = models.CharField(max_length=30)
    is_container = models.BooleanField(default=False, verbose_name="Can contain assets")
    asset_manufacturer = models.ForeignKey(AssetManufacturer, on_delete=models.PROTECT)
    history = HistoricalRecords()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def display_name(self) -> str:
        if self.asset_manufacturer.name == "Inventory":
            return self.name
        return f"{self.asset_manufacturer.name} {self.name}"

    def __str__(self) -> str:
        return self.display_name

    def get_absolute_url(self):
        return reverse("inventory:model_view", args=[self.pk])

    def get_edit_url(self):
        return reverse("inventory:model_edit", args=[self.pk])

    def get_delete_url(self):
        return reverse("inventory:model_delete", args=[self.pk])


def location_validator(val):
    try:
        asset = Asset.objects.filter(pk=val).get()
    except Exception:
        raise ValidationError("Not a valid asset.")

    if not asset.asset_model.is_container:
        raise ValidationError(f"{asset} is not a container.")




class Asset(models.Model):
    """An individual instance of a assetmodel."""

    class Condition(models.TextChoices):
        """The condition of an item."""

        UNKNOWN = "U"
        BROKEN = "B"
        DISPOSED = "D"
        NEEDS_ASSEMBLY = "A"
        NEEDS_REPAIR = "R"
        WORKING = "W"

    asset_code = models.CharField(
        max_length=11,
        unique=True,
        validators=[validate_asset_code],
        default=generate_asset_code,
    )
    name = models.CharField(max_length=30, null=True, blank=True)
    location = models.ForeignKey(
        "Asset",
        on_delete=models.PROTECT,
        validators=[location_validator],
        null=True,  # Rely on validation in clean
        limit_choices_to={"asset_model__is_container": True},
    )
    asset_model = models.ForeignKey(AssetModel, on_delete=models.PROTECT)
    condition = models.CharField(
        max_length=2, choices=Condition.choices, default=Condition.UNKNOWN,
    )
    history = HistoricalRecords()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    audited_at = models.DateTimeField()

    consumable_models = models.ManyToManyField("ConsumableModel", through="Consumable")

    @property
    def display_name(self) -> str:
        if self.name is None or len(self.name) == 0:
            return self.asset_model.display_name
        else:
            return self.name

    def __str__(self) -> str:
        return f"{self.display_name} ({self.asset_code})"

    def get_absolute_url(self):
        return reverse("inventory:asset_view", args=[self.asset_code])

    def get_edit_url(self):
        return reverse("inventory:asset_edit", args=[self.asset_code])

    def get_delete_url(self):
        return reverse("inventory:asset_delete", args=[self.asset_code])

    def clean(self):
        """Validate the model."""
        
        if self.location_id is None and self.asset_code[4:10] != 'WOR-LD':
            # Check that the location is not null, unless it's a world location.
            raise ValidationError("Assets must have a valid location.")

        if self.location and self.location == self:
            # Only the world can be within itself
            if self.asset_code[4:10] != 'WOR-LD':
                raise ValidationError("Assets cannot be stored within themselves.")
        else:
            # The world must be within itself
            if self.asset_code[4:10] == 'WOR-LD':
                raise ValidationError(f"DimensionError: {self.location} is not a TARDIS")


class ConsumableModel(models.Model):
    """The model of a consumable asset."""

    name = models.CharField(max_length=30)
    asset_manufacturer = models.ForeignKey(AssetManufacturer, on_delete=models.PROTECT)
    history = HistoricalRecords()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    locations = models.ManyToManyField("Asset", through="Consumable")

    @property
    def display_name(self) -> str:
        if self.asset_manufacturer.name == "Inventory":
            return self.name
        return f"[C] {self.asset_manufacturer.name} {self.name}"

    def __str__(self) -> str:
        return self.display_name

    def get_total(self) -> int:
        return self.consumable_set.aggregate(quantity=models.Sum("quantity")).get(
            "quantity"
        )

    def get_absolute_url(self):
        return reverse("inventory:consumablemodel_view", args=[self.pk])

    def get_edit_url(self):
        return reverse("inventory:consumablemodel_edit", args=[self.pk])

    def get_delete_url(self):
        return reverse("inventory:consumablemodel_delete", args=[self.pk])


class Consumable(models.Model):
    """A count of a consumable asset in a location."""

    location = models.ForeignKey(
        "Asset",
        on_delete=models.PROTECT,
        limit_choices_to={"asset_model__is_container": True},
    )
    consumable_model = models.ForeignKey("ConsumableModel", on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)
    history = HistoricalRecords()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.quantity} × {self.consumable_model.name}"

    def get_edit_url(self):
        return reverse("inventory:consumable_edit", args=[self.pk])
