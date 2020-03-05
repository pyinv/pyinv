"""Accounts middlware."""

from django.middleware.common import MiddlewareMixin
from django.shortcuts import reverse
from django.http.response import HttpResponseRedirect


class ProfileRequiredMiddleware(MiddlewareMixin):
    """Ensure that users have filled out their profile."""

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated \
                and (not request.user.first_name \
                     or not request.user.last_name \
                     or not request.user.email) \
                and not request.path.startswith(reverse('accounts:profile')):
            return HttpResponseRedirect(reverse("accounts:profile"))
        return None
