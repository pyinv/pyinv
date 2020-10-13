from django.shortcuts import redirect


def index(request):
    return redirect("inventory:asset_search")
