from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Main dashboard view, requires authentication. If there's no logged in user,
# Django automatially redirecst them to /accounts/login URL.
@login_required
def dashboard_home(request):
    return render(request, "dashboard/home.html")
    