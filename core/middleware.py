from django.shortcuts import redirect
from django.urls import reverse


class SuperuserRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logout_url = reverse("logout")

        if request.user.is_authenticated and request.user.is_superuser:
            if not (
                request.path == "/" or
                request.path.startswith("/admin") or
                request.path == logout_url
            ):
                return redirect("/")

        return self.get_response(request)