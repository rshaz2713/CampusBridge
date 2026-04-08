from django.shortcuts import render, redirect
from core.services.auth import AuthService
from core.forms.registration_form import CampusBridgeRegisterForm

def register_view(request):
    if request.method == "POST":
        user, form = AuthService.register_user(request)
        if user:
            return redirect("dashboard_home")
    else:
        form = CampusBridgeRegisterForm()
    
    return render(request, "registration/register.html", {"form": form})