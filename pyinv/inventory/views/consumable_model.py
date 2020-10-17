from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from inventory.models import Consumable, ConsumableModel


class ConsumableModelCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = ConsumableModel
    template_name = "inventory/consumablemodel_create.html"
    fields = ["name", "asset_manufacturer", "notes"]

    permission_required = "inventory.add_consumable_model"
    permission_denied_message = "You do not have permission to create consumable models."

    def get_success_url(self):
        return self.object.get_absolute_url()


class ConsumableModelDisplayView(LoginRequiredMixin, DetailView):

    model = ConsumableModel
    template_name = "inventory/consumablemodel_view.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)

        data["consumables"] = Consumable.objects.filter(
            consumable_model=self.object
        ).order_by("-updated_at").all()
        return data


class ConsumableModelUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateView
):

    model = ConsumableModel
    template_name = "inventory/consumablemodel_edit.html"

    fields = ["name", "asset_manufacturer", "notes"]

    permission_required = "inventory.change_consumable_model"
    permission_denied_message = (
        "You do not have permission to update consumable models."
    )

    def get_success_url(self):
        return self.object.get_absolute_url()


class ConsumableModelDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteView
):

    model = ConsumableModel
    template_name = "inventory/consumablemodel_delete.html"

    fields = ["name", "notes"]

    permission_required = "inventory.delete_consumable_model"
    permission_denied_message = (
        "You do not have permission to delete consumable models."
    )

    def get_success_url(self):
        return self.object.asset_manufacturer.get_absolute_url()
