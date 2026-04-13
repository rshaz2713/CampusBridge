from datetime import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core.models import Profile
from .models import StudentRecord, ProfessorRecord, Course, Announcement, AnnouncementRead


#This will show the professors announcements on the students dashboard
@login_required
def dashboard_home(request):
    role = request.user.profile.role

    # get unread announcements for this user
    unread_announcements = Announcement.objects.exclude(
        announcementread__user=request.user,
        announcementread__is_read=True
    )

    return render(request, "dashboard/home.html", {
        "role": role,
        "announcements": unread_announcements
    })

    role = profile.role
    hour = datetime.now().hour

    if hour < 12:
        greeting = "Good Morning"
    elif hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    return render(request, "dashboard/home.html", {
        "role": role,
        "greeting": greeting
    })

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "message"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter announcement title"
            }),
            "message": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter announcement message",
                "rows": 4
            }),
        }
        
# This adds the professor announcement view
@login_required
def create_announcement_view(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": "student"}
    )

    if profile.role != "professor":
        return render(request, "dashboard/access_denied.html")

    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.professor = request.user
            announcement.save()
            return redirect("dashboard_home")
    else:
        form = AnnouncementForm()

    return render(request, "dashboard/create_announcement.html", {"form": form})


@login_required
def announcement_list_view(request):
    announcements = Announcement.objects.all().order_by("-created_at")
    return render(request, "dashboard/professor_announcement.html", {"announcements": announcements})


@login_required
def announcement_detail_view(request, announcement_id):
    announcement = Announcement.objects.get(id=announcement_id)

    # mark as read
    AnnouncementRead.objects.update_or_create(
        user=request.user,
        announcement=announcement,
        defaults={'is_read': True}
    )

    return render(request, "dashboard/announcement_details.html", {
        "announcement": announcement
    })




@login_required
def degree_audit_view(request):
    record = StudentRecord.objects.filter(user=request.user).first()
    return render(request, "dashboard/degree_audit.html", {"record": record})

@login_required
def professor_search_view(request):
    query = request.GET.get("q", "").strip()
    all_students = StudentRecord.objects.all().order_by("student_id")
    search_results = StudentRecord.objects.none()

    if query:
        if query.isdigit():
            search_results = StudentRecord.objects.filter(student_id=int(query))
        else:
            search_results = StudentRecord.objects.filter(full_name__icontains=query)

    return render(request, "dashboard/professor_search.html", {
        "query": query,
        "search_results": search_results,
        "all_students": all_students,
    })
