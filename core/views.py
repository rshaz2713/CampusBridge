from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms.registration_form import CampusBridgeRegisterForm

def home(request):
    return render(request, "core/home.html")

def register_view(request):
    if request.method == "POST":
        form = CampusBridgeRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard_home")
    else:
        form = CampusBridgeRegisterForm()

    return render(request, "registration/register.html", {"form": form})