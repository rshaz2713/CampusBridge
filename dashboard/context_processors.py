from core.models import Profile
from .models import Announcement, AnnouncementRead


def announcement_notifications(request):
    if not request.user.is_authenticated:
        return {
            "announcements": [],
            "unread_announcements": [],
            "role": None,
            "current_institution": None,
            "institution_options": [],
        }

    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": "student"}
    )

    role = profile.role

    current_institution = request.session.get("institution", "CCSU")
    institution_options = ["CCSU", "UConn", "Tunxis"]

    if role == "student":
        all_announcements = Announcement.objects.all().order_by("-created_at")

        read_ids = AnnouncementRead.objects.filter(
            user=request.user,
            is_read=True
        ).values_list("announcement_id", flat=True)

        unread_announcements = all_announcements.exclude(id__in=read_ids)

        return {
            "announcements": all_announcements[:5],
            "unread_announcements": unread_announcements[:5],
            "role": role,
            "current_institution": current_institution,
            "institution_options": institution_options,
        }

    return {
        "announcements": [],
        "unread_announcements": [],
        "role": role,
        "current_institution": current_institution,
        "institution_options": institution_options,
    }