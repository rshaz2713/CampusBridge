from core.models import InstitutionMembership
from .models import Announcement, AnnouncementRead


def institution_context(request):
    if not request.user.is_authenticated:
        return {
            "current_institution": None,
            "current_membership": None,
            "institution_options": [],
            "role": None,
        }

    memberships = (
        InstitutionMembership.objects
        .filter(user=request.user)
        .select_related("institution")
        .order_by("institution__name", "role")
    )

    current_membership = None
    current_membership_id = request.session.get("current_membership_id")

    if current_membership_id:
        current_membership = memberships.filter(id=current_membership_id).first()

    if current_membership is None:
        current_membership = memberships.first()

        if current_membership:
            request.session["current_membership_id"] = current_membership.id
            request.session["current_institution_id"] = current_membership.institution_id

    return {
        "current_membership": current_membership,
        "current_institution": current_membership.institution if current_membership else None,
        "institution_options": memberships,
        "role": current_membership.role if current_membership else None,
    }


def announcement_notifications(request):
    if not request.user.is_authenticated:
        return {
            "announcements": [],
            "unread_announcements": [],
        }

    current_institution_id = request.session.get("current_institution_id")

    if not current_institution_id:
        return {
            "announcements": [],
            "unread_announcements": [],
        }

    announcements = (
        Announcement.objects
        .filter(institution_id=current_institution_id)
        .order_by("-created_at")
    )

    read_ids = AnnouncementRead.objects.filter(
        user=request.user,
        is_read=True,
        announcement__institution_id=current_institution_id,
    ).values_list("announcement_id", flat=True)

    unread_announcements = announcements.exclude(id__in=read_ids)

    return {
        "announcements": announcements[:5],
        "unread_announcements": unread_announcements[:5],
    }