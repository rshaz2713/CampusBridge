from django.shortcuts import render, redirect
from core.services.auth import AuthService

def register_view(request):
    if request.method == "POST":
        user, form = AuthService.register_user(request)
        if user:
            return redirect("dashboard_home")
    else:
        from core.forms.registration_form import CampusBridgeRegisterForm
        form = CampusBridgeRegisterForm()
    return render(request, "registration/register.html", {"form": form})