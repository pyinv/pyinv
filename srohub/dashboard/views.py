from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def index(request):
    # return render(request, "dashboard/index.html")
    return redirect("inventory:index")
