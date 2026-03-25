from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Main dashboard view, requires authentication. If there's no logged in user,
# Django automatially redirecst them to /accounts/login URL.
@login_required
def dashboard_home(request):

    # Testing for role-based rendering, hard-coded for now.
    # This placeholder is used until perssitent role data is implemetned elsewhere. 
    role = request.session.get("role", "student")
    context = {
        "role": role,
    }

    return render(request, "dashboard/home.html", context)
    