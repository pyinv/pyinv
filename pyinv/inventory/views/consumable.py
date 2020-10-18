from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, ListView
from inventory.models import Consumable


class ConsumableSearchView(LoginRequiredMixin, ListView):

    model = Consumable
    template_name = "inventory/consumable_search.html"
    paginate_by = 15

    # There is no display view for a consumable
    # def get(self, request, *args, **kwargs):
    #     """If there is exactly one result, redirect us to it."""
    #     response = super().get(request, *args, **kwargs)
    #     if self.object_list.count() == 1:
    #         return redirect(self.object_list.get())
    #     return response

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)
        if "query" in self.request.GET:
            data["query"] = self.request.GET["query"]
        return data

    def get_queryset(self):
        if "query" in self.request.GET and self.request.GET["query"] != "":
            return Consumable.get_search_queryset(self.request.GET["query"])
        else:
            return Consumable.objects.order_by("-updated_at").all()


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
