from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Profile
from datetime import datetime
from core.constants.resources import RESOURCE_INFO

# Main dashboard view, requires authentication. If there's no logged in user,
# Django automatially redirects them to /accounts/login URL.

@login_required
def dashboard_home(request):
    profile = Profile.objects.get(user=request.user)
    role = profile.role

    resources = [
        {'id': key, **value}
        for key, value in RESOURCE_INFO.items()
        if role in value["roles"]
    ]
    
    from datetime import datetime
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    pinned_ids_ordered = list(profile.pinned_resources.values_list('resource_id', flat=True))

    context = {
        'user': request.user,
        'role': role,
        'greeting': greeting,
        'pinned_urls': pinned_ids_ordered,
        'resources': resources,
    }

    return render(request, 'dashboard/home.html', context)
