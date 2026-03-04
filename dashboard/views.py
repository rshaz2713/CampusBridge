from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.

@login_required
def dashboard_home(request):
    return HttpResponse(f"Dashboard running. Logged in as {request.user.username}.")