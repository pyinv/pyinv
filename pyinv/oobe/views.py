from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin, UserPassesTestMixin
from django.db.utils import OperationalError
from django.contrib import messages
from dynamic_preferences.registries import global_preferences_registry

import damm32
from datetime import datetime

from inventory.models import Asset, AssetManufacturer, AssetModel

from .forms import OOBEForm

global_preferences = global_preferences_registry.manager()

class OOBECheckMixin(UserPassesTestMixin, generic.View):
    def test_func(self):
        world = Asset.objects.filter(
            asset_code__regex="^[A-Z0-9]{3}-WOR-LD[A-Z0-9]$"
        ).exists()
        return self.request.user.is_superuser and not world


class OOBE(LoginRequiredMixin, OOBECheckMixin, generic.FormView):

    template_name = "oobe/index.html"
    form_class = OOBEForm
    success_url = "/"
    
    try: 
        initial = {
            "title": global_preferences["general__title"],
            "inventory_org": global_preferences["inventory_org"],
        }
    except OperationalError:
        initial = {}

    def form_valid(self, form):

        d32 = damm32.Damm32()

        global_preferences["general__title"] = form.data["title"]
        global_preferences["inventory_org"] = form.data["inventory_org"]

        man = AssetManufacturer(name=form.data["inventory_org"])
        man.save()

        model = AssetModel(name="Location", is_container=True, asset_manufacturer=man)
        model.save()

        code = form.data["inventory_org"] + "WORLD"
        code += d32.calculate(code)

        world = Asset(
            name="World",
            asset_code=f"{code[:3]}-{code[3:6]}-{code[6:9]}",
            location_id=None,
            asset_model=model,
            condition="U",
            notes="The world. The root location for everything.",
            audited_at=datetime.now()
        )
        world.save()

        world.location = world
        world.save()

        if "onboarding" in self.request.session:
            self.request.session.pop("onboarding")
        messages.success(self.request, "PyInv has been successfully setup!")
        return super().form_valid(form)
