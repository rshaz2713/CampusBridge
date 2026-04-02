from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms
from .models import Profile

# Registration form
class CampusBridgeRegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-control custom-input"
        })
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control custom-input",
            "placeholder": "Enter first name"
        })
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control custom-input",
            "placeholder": "Enter last name"
        })
    )

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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
            role = self.cleaned_data["role"]
            user.profile.role = role
            user.profile.save()

        return user

# Create your views here.

# CampusBridge home view
def home(request):
    return render(request, "core/home.html")

# Registration view
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
