from django.contrib import admin
from pyotp import random_base32

from .models import AccessCode


@admin.register(AccessCode)
class AccessCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'counter', 'length')

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(AccessCodeAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['secret'].initial = random_base32()
        return form
