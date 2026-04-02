from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Profile
from datetime import datetime

# Main dashboard view, requires authentication. If there's no logged in user,
# Django automatially redirecst them to /accounts/login URL.

@login_required
def dashboard_home(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": "student"}
    )

    role = profile.role
    hour = datetime.now().hour

    if hour < 12:
        greeting = "Good Morning"
    elif hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    return render(request, "dashboard/home.html", {
        "role": role,
        "greeting": greeting
    })
    