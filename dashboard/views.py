from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Profile
from datetime import datetime

# Main dashboard view, requires authentication. If there's no logged in user,
# Django automatially redirecst them to /accounts/login URL.



@login_required
def dashboard_home(request):
    profile = Profile.objects.get(user=request.user)
    role = profile.role
    
    from datetime import datetime
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    pinned_resources = profile.pinned_resources.all()[:6]
    pinned_urls = list(profile.pinned_resources.values_list('url', flat=True))
    
    # ✅ ADD THESE DEBUG LINES HERE
    print(f"DEBUG: pinned_urls = {pinned_urls}")
    print(f"DEBUG: pinned_resources count = {pinned_resources.count()}")
    
    context = {
        'user': request.user,
        'role': role,
        'greeting': greeting,
        'pinned_resources': pinned_resources,
        'pinned_urls': pinned_urls,
    }
    
    return render(request, 'dashboard/home.html', context)

# @login_required
# def dashboard_home(request):
#     profile, created = Profile.objects.get_or_create(
#         user=request.user,
#         defaults={"role": "student"}
#     )

#     role = profile.role
#     hour = datetime.now().hour

#     if hour < 12:
#         greeting = "Good Morning"
#     elif hour < 18:
#         greeting = "Good Afternoon"
#     else:
#         greeting = "Good Evening"

#     return render(request, "dashboard/home.html", {
#         "role": role,
#         "greeting": greeting
#     })
    