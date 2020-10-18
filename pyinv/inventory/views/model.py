from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView
from inventory.models import AssetModel


class AssetModelSearchView(LoginRequiredMixin, ListView):

    model = AssetModel
    template_name = "inventory/model_search.html"
    paginate_by = 15

    def get(self, request, *args, **kwargs):
        """If there is exactly one result, redirect us to it."""
        response = super().get(request, *args, **kwargs)
        if self.object_list.count() == 1:
            return redirect(self.object_list.get())
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)
        if "query" in self.request.GET:
            data["query"] = self.request.GET["query"]
        return data

    def get_queryset(self):
        if "query" in self.request.GET and self.request.GET["query"] != "":
            return AssetModel.get_search_queryset(self.request.GET["query"])
        else:
            return AssetModel.objects.order_by("-updated_at").all()


class AssetModelDisplayView(LoginRequiredMixin, DetailView):

    model = AssetModel
    template_name = "inventory/model_view.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)

        if "page" in self.request.GET:
            page_num = self.request.GET["page"]
        else:
            page_num = 1

        assets = self.object.asset_set.order_by("-updated_at").all()
        paginator = Paginator(assets, 20)
        data["page_obj"] = paginator.get_page(page_num)
        data["is_paginated"] = True
        return data


class AssetModelCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = AssetModel
    template_name = "inventory/model_create.html"
    fields = ["name", "asset_manufacturer", "is_container", "notes"]

    permission_required = "inventory.add_asset_model"
    permission_denied_message = "You do not have permission to create asset models."

    def get_success_url(self):
        return self.object.get_absolute_url()


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
