from django.contrib import admin

from .models import AccessCode


@admin.register(AccessCode)
class AccessCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'counter')

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(AccessCodeAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['secret'].initial = "bees"
        return form
