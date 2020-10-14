"""Accounts middlware."""

from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.middleware.common import MiddlewareMixin
from django.shortcuts import reverse

from inventory.models import Asset


class OOBEMiddleware(MiddlewareMixin):
    """Check if OOBE is needed."""

    def process_view(self, request, view_func, view_args, view_kwargs):
        if (
            not Asset.objects.filter(asset_code__regex="^[A-Z0-9]{3}-WOR-LD[A-Z0-9]$").exists()
            and not request.path.startswith(reverse("oobe:index"))
            and not request.path.startswith("/auth")
        ):
            request.session["oobe"] = True
            return HttpResponseRedirect(reverse("oobe:index"))
        return None
