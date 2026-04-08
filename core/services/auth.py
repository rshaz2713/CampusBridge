from django.contrib.auth import login, logout
from core.forms.registration_form import CampusBridgeRegisterForm
from django.http import JsonResponse

class AuthService:
    @staticmethod
    def register_user(request):
        form = CampusBridgeRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return user, None
        return None, form

    @staticmethod
    def extend_session(request, session_age):
        request.session.set_expiry(session_age)
        request.session.modified = True
        return JsonResponse({
            "ok": True,
            "remaining_seconds": request.session.get_expiry_age(),
        })

    @staticmethod
    def expire_session(request):
        logout(request)
        return JsonResponse({"ok": True})