from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.views.generic import CreateView, UpdateView
from inventory.models import Consumable


class ConsumableCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = Consumable
    template_name = "inventory/consumable_create.html"
    fields = ["consumable_model", "location", "quantity", "notes"]

    permission_required = "inventory.add_consumable"
    permission_denied_message = "You do not have permission to create consumables."

    def get_success_url(self):
        return self.object.location.get_absolute_url()


class ConsumableUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = Consumable
    template_name = "inventory/consumable_edit.html"

    fields = ["consumable_model", "location", "quantity", "notes"]

    permission_required = "inventory.change_consumable"
    permission_denied_message = "You do not have permission to update consumables."

    def get_success_url(self):
        return self.object.location.get_absolute_url()
