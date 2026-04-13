from core.models import Profile
from .models import Announcement

# This context processor will make the announcements available in all templates for students
def announcement_notifications(request):
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(
            user=request.user,
            defaults={"role": "student"}
        )

        if profile.role == "student":
            announcements = Announcement.objects.all().order_by("-created_at")[:5]
        else:
            announcements = Announcement.objects.none()

        return {
            "announcements": announcements,
            "role": profile.role,
        }

    return {
        "announcements": [],
        "role": None,
    }