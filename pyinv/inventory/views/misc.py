from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView
from inventory.models import Asset


class SearchView(LoginRequiredMixin, TemplateView):

    template_name = "inventory/search.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if "query" in self.request.GET:
            data["query"] = self.request.GET["query"]
            data["assets"] = Asset.get_search_queryset(self.request.GET["query"])[:10]
        return data
