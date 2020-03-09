from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse

from .models import Asset, AssetModel, AssetManufacturer


class InventorySearchView(LoginRequiredMixin, ListView):

    model = Asset
    template_name = "inventory/search.html"
    paginate_by = 15

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)
        if 'query' in self.request.GET:
            data['query'] = self.request.GET['query']
        return data

    def get_queryset(self):
        if 'query' in self.request.GET:
            return Asset.objects.filter(
                Q(name__icontains=self.request.GET['query']) |
                Q(notes__icontains=self.request.GET['query']) |
                Q(asset_code__icontains=self.request.GET['query']) |
                Q(asset_model__name__icontains=self.request.GET['query']) |
                Q(asset_model__asset_manufacturer__name__icontains=self.request.GET['query']),
                ~Q(condition="D")  # Ignore disposed assets.
            ).order_by("-updated_at")
        else:
            return Asset.objects.all()


class AssetDisplayView(LoginRequiredMixin, DetailView):

    model = Asset
    template_name = "inventory/asset_view.html"
    slug_field = "asset_code"
    slug_field_kwarg = "asset_code"

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)

        if 'page' in self.request.GET:
            page_num = self.request.GET['page']
        else:
            page_num = 1

        assets = self.object.asset_set.filter(~Q(asset_code=self.object.asset_code)).order_by("-updated_at")
        paginator = Paginator(assets, 20)
        data['page_obj'] = paginator.get_page(page_num)
        data['is_paginated'] = self.object.asset_model.is_container
        return data


class AssetUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = Asset
    template_name = "inventory/asset_edit.html"
    slug_field = "asset_code"
    slug_field_kwarg = "asset_code"

    fields = ["name", "asset_model", "condition", "location", "notes"]

    permission_required = "inventory.change_asset"
    permission_denied_message = "You do not have permission to update assets."

    def get_success_url(self):
        return self.object.get_absolute_url()


class AssetDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = Asset
    template_name = "inventory/asset_delete.html"
    slug_field = "asset_code"
    slug_field_kwarg = "asset_code"

    fields = ["name", "asset_model", "condition", "location", "notes"]

    permission_required = "inventory.delete_asset"
    permission_denied_message = "You do not have permission to delete assets."

    def get_success_url(self):
        return self.object.location.get_absolute_url()


class AssetModelDisplayView(LoginRequiredMixin, DetailView):

    model = AssetModel
    template_name = "inventory/model_view.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)

        if 'page' in self.request.GET:
            page_num = self.request.GET['page']
        else:
            page_num = 1

        assets = self.object.asset_set.order_by("-updated_at").all()
        paginator = Paginator(assets, 20)
        data['page_obj'] = paginator.get_page(page_num)
        data['is_paginated'] = True
        return data


class AssetModelUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = AssetModel
    template_name = "inventory/model_edit.html"

    fields = ["name", "asset_manufacturer", "is_container", "notes"]

    permission_required = "inventory.change_asset_model"
    permission_denied_message = "You do not have permission to update asset models."

    def get_success_url(self):
        return self.object.get_absolute_url()


class AssetModelDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = AssetModel
    template_name = "inventory/model_delete.html"

    fields = ["name", "asset_manufacturer", "is_container", "notes"]

    permission_required = "inventory.delete_asset_model"
    permission_denied_message = "You do not have permission to delete asset models."

    def get_success_url(self):
        return self.object.asset_manufacturer.get_absolute_url()


class AssetManufacturerDisplayView(LoginRequiredMixin, DetailView):

    model = AssetManufacturer
    template_name = "inventory/manufacturer_view.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)

        if 'page' in self.request.GET:
            page_num = self.request.GET['page']
        else:
            page_num = 1
        assets = self.object.assetmodel_set.order_by("-updated_at").all()
        paginator = Paginator(assets, 20)
        data['page_obj'] = paginator.get_page(page_num)
        data['is_paginated'] = True
        return data


class AssetManufacturerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = AssetManufacturer
    template_name = "inventory/manufacturer_edit.html"

    fields = ["name", "notes"]

    permission_required = "inventory.change_asset_manufacturer"
    permission_denied_message = "You do not have permission to update manufacturers."

    def get_success_url(self):
        return self.object.get_absolute_url()


class AssetManufacturerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = AssetManufacturer
    template_name = "inventory/manufacturer_delete.html"

    fields = ["name", "notes"]

    permission_required = "inventory.delete_asset_manufacturer"
    permission_denied_message = "You do not have permission to delete manufacturers."

    def get_success_url(self):
        return reverse("inventory:index")
