from django.utils import timezone

# Adds remaining session time to all templates for authenticated users.
def session_timeout_info(request):
    remaining_seconds = None

    if request.user.is_authenticated:
        expiry = request.session.get_expiry_date()
        remaining_seconds = max(0, int((expiry - timezone.now()).total_seconds()))

    return {
        "session_seconds_remaining": remaining_seconds
    }
