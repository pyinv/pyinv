from django.views.generic import DetailView, ListView
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Asset, AssetModel, AssetManufacturer


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
                Q(asset_code__icontains=self.request.GET['query']) |
                Q(asset_model__name__icontains=self.request.GET['query']) |
                Q(asset_model__asset_manufacturer__name__icontains=self.request.GET['query']),
            ).order_by("-updated_at")
        else:
            return Asset.objects.all()


class AssetDisplayView(DetailView):

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


class AssetModelDisplayView(DetailView):

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


class AssetManufacturerDisplayView(DetailView):

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
