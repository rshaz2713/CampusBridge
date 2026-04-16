from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from core.models import Profile, PinnedResource
from core.constants.resources import RESOURCE_INFO

@login_required
def toggle_pin(request, resource_id):
    if request.method != "POST":
        return redirect('dashboard_home')
    
    profile = request.user.profile

    resource_info = RESOURCE_INFO.get(resource_id, {
        'title': resource_id.replace('-', ' ').title(),
        'url': '#',
        'description': ''
    })

    existing = PinnedResource.objects.filter(
        profile=profile,
        resource_id=resource_id
    )

    if existing.exists():
        existing.delete()
    else:
        PinnedResource.objects.create(
            profile=profile,
            resource_id=resource_id,
            url=resource_info['url'],
            title=resource_info['title'],
            description=resource_info['description']
        )

    return redirect('dashboard_home')