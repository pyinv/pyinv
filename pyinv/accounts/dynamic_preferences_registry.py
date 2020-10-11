from re import match

from django.core.exceptions import ValidationError
from dynamic_preferences.types import BooleanPreference, StringPreference, Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.users.registries import user_preferences_registry

general = Section('general')

@global_preferences_registry.register
class SiteTitle(StringPreference):
    section = general
    name = 'title'
    default = 'PyInv'

@global_preferences_registry.register
class InventoryOrg(StringPreference):
    name = 'inventory_org'
    default = 'INV'

    def validate(self, value):
        if not match("^[A-Z]{3}$", value):
            raise ValidationError("Must consist of three capital letters")