
# views.py
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from ..models import Profile, PinnedResource



# core/views.py
@login_required
def toggle_pin(request, resource_id):
    if request.method != "POST":
        return redirect('dashboard_home')
    
    profile = Profile.objects.get(user=request.user)
    
    RESOURCE_INFO = {
        'wellness': {
            'title': 'Wellness Services',
            'url': 'https://www.ccsu.edu/student-wellness-services',
            'description': 'Access mental health and wellness support.'
        },
        'degree-audit': {
            'title': 'Degree Audit',
            'url': '#',
            'description': 'Track your academic progress and plan courses.'
        },
        'financial-docs': {
            'title': 'Financial Documents',
            'url': '#',
            'description': 'View tuition, aid packages, and tax documents.'
        },
        'search-student': {
            'title': 'Search Student',
            'url': '#',
            'description': 'Find students by name or ID.'
        },
        'announcements': {
            'title': 'Announcements',
            'url': '#',
            'description': 'View faculty announcements.'
        },
        'course-management': {
            'title': 'Course Management',
            'url': '#',
            'description': 'Manage course materials and grading.'
        },
    }
    
    resource_info = RESOURCE_INFO.get(resource_id, {
        'title': resource_id.title().replace('-', ' '),
        'url': '#',
        'description': ''
    })
    
    try:
        pin = PinnedResource.objects.get(profile=profile, resource_id=resource_id)
        pin.delete()
    except PinnedResource.DoesNotExist:
        PinnedResource.objects.create(
            profile=profile,
            resource_id=resource_id,       # ✅ Store resource_id for unpin URL
            url=resource_info['url'],       # ✅ Store actual URL for Visit button
            title=resource_info['title'],
            description=resource_info['description']
        )
    
    return redirect('dashboard_home')