from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from core.services.auth import AuthService
from config import settings

@login_required
@require_POST
def extend_session(request):
    return AuthService.extend_session(request, settings.SESSION_COOKIE_AGE)

@login_required
@require_POST
def expire_session(request):
    return AuthService.expire_session(request)