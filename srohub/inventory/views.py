from django.views.generic.list import ListView
from django.db.models import Q

from .models import Asset


class InventorySearchView(ListView):

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
                Q(asset_code__icontains=self.request.GET['query']),
            )
        else:
            return Asset.objects.all()
