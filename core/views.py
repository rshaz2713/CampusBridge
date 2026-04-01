from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings

# Registration form
class CampusBridgeRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control custom-input",
            "placeholder": "Enter username"
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control custom-input",
            "placeholder": "Enter password"
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control custom-input",
            "placeholder": "Confirm password"
        })
    )

# Create a user for registration
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

# Render the CampusBridge page
def home(request):
    return render(request, "core/home.html")
    
# Extend session
@login_required
@require_POST
def extend_session(request):
    request.session.set_expiry(settings.SESSION_COOKIE_AGE)
    request.session.modified = True

    return JsonResponse({
        "ok": True,
        "remaining_seconds": request.session.get_expiry_age(),
    })

# Force session timeout upon expiry
@login_required
@require_POST
def expire_session(request):
    logout(request)
    return JsonResponse({
        "ok": True
    })