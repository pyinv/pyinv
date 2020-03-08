from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    # return render(request, "dashboard/index.html")
    return redirect("inventory:index")

