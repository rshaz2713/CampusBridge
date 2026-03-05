from django.shortcuts import render

# Landing page view when user loads CampusBridge.
def home(request):
    return render(request, "core/home.html")
    