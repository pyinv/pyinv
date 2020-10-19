from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView
from inventory.models import Asset, AssetModel, AssetManufacturer, Consumable, ConsumableModel


class SearchView(LoginRequiredMixin, TemplateView):

    template_name = "inventory/search.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if "query" in self.request.GET:
            query = self.request.GET["query"]
            data["query"] = query
        else:
            query = ""

        data["assets_count"] = Asset.get_search_queryset(query).count()
        data["assets"] = Asset.get_search_queryset(query)[:2]
        data["models_count"] = AssetModel.get_search_queryset(query).count()
        data["models"] = AssetModel.get_search_queryset(query)[:2]
        data["manufacturers_count"] = AssetManufacturer.get_search_queryset(query).count()
        data["manufacturers"] = AssetManufacturer.get_search_queryset(query)[:2]
        data["consumables_count"] = Consumable.get_search_queryset(query).count()
        data["consumables"] = Consumable.get_search_queryset(query)[:2]
        # data["consumablemodels"] = ConsumableModel.get_search_queryset(self.request.GET["query"])

        data["count_sum"] = sum([
            data["assets_count"],
            data["models_count"],
            data["manufacturers_count"],
            data["consumables_count"],
        ])
        return data
