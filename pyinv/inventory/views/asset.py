from datetime import datetime

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import HiddenInput
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from inventory.models import Asset, Consumable


class AssetSearchView(LoginRequiredMixin, ListView):

    model = Asset
    template_name = "inventory/asset_search.html"
    paginate_by = 15

    def get(self, request, *args, **kwargs):
        """If there is exactly one result, redirect us to it."""
        response = super().get(request, *args, **kwargs)
        if self.object_list.count() == 1:
            target_asset = self.object_list.get()
            return redirect(
                "inventory:asset_view",
                slug=target_asset.asset_code,
            )
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)
        if "query" in self.request.GET:
            data["query"] = self.request.GET["query"]
        return data

    def get_queryset(self):
        if "query" in self.request.GET and self.request.GET["query"] != "":
            return Asset.objects.filter(
                Q(name__icontains=self.request.GET["query"])
                | Q(notes__icontains=self.request.GET["query"])
                | Q(asset_code__icontains=self.request.GET["query"])
                | Q(asset_model__name__icontains=self.request.GET["query"])
                | Q(
                    asset_model__asset_manufacturer__name__icontains=self.request.GET[
                        "query"
                    ]
                ),
                ~Q(condition="D"),  # Ignore disposed assets.
            ).order_by("-updated_at")
        else:
            return Asset.objects.order_by("-updated_at").all()


class AssetDisplayView(LoginRequiredMixin, DetailView):

    model = Asset
    template_name = "inventory/asset_view.html"
    slug_field = "asset_code"
    slug_field_kwarg = "asset_code"

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)

        if "page" in self.request.GET:
            page_num = self.request.GET["page"]
        else:
            page_num = 1

        assets = self.object.asset_set.filter(
            ~Q(asset_code=self.object.asset_code)
        ).order_by("-updated_at")
        paginator = Paginator(assets, 20)
        data["page_obj"] = paginator.get_page(page_num)
        data["is_paginated"] = self.object.asset_model.is_container
        data["consumables"] = Consumable.objects.filter(
            location=self.object,
        ).order_by("-updated_at").all()
        return data


class AssetCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = Asset
    template_name = "inventory/asset_create.html"
    fields = [
        "asset_code",
        "name",
        "location",
        "asset_model",
        "condition",
        "notes",
        "audited_at",
    ]
    initial = {"audited_at": datetime.now()}

    permission_required = "inventory.add_asset"
    permission_denied_message = "You do not have permission to create assets."

    def get_form(self, form_class=None):
        form = super(AssetCreateView, self).get_form(form_class)
        form.fields['audited_at'].widget = HiddenInput()
        return form

    def get_success_url(self):
        return self.object.get_absolute_url()


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
