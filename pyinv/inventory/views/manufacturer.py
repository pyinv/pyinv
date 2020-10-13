from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from inventory.models import AssetManufacturer


class AssetManufacturerDisplayView(LoginRequiredMixin, DetailView):

    model = AssetManufacturer
    template_name = "inventory/manufacturer_view.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)

        if "page" in self.request.GET:
            page_num = self.request.GET["page"]
        else:
            page_num = 1
        assets = self.object.assetmodel_set.order_by("-updated_at").all()
        paginator = Paginator(assets, 20)
        data["page_obj"] = paginator.get_page(page_num)
        data["is_paginated"] = True
        return data


class AssetManufacturerCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):

    model = AssetManufacturer
    template_name = "inventory/manufacturer_create.html"
    fields = ["name", "notes"]

    permission_required = "inventory.add_asset_manufacturer"
    permission_denied_message = "You do not have permission to create asset manufacturers"

    def get_success_url(self):
        return self.object.get_absolute_url()


class AssetManufacturerUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateView
):

    model = AssetManufacturer
    template_name = "inventory/manufacturer_edit.html"

    fields = ["name", "notes"]

    permission_required = "inventory.change_asset_manufacturer"
    permission_denied_message = "You do not have permission to update manufacturers."

    def get_success_url(self):
        return self.object.get_absolute_url()


class AssetManufacturerDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteView
):

    model = AssetManufacturer
    template_name = "inventory/manufacturer_delete.html"

    fields = ["name", "notes"]

    permission_required = "inventory.delete_asset_manufacturer"
    permission_denied_message = "You do not have permission to delete manufacturers."

    def get_success_url(self):
        return reverse("inventory:index")
