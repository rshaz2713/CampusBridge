from datetime import datetime
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core.models import Profile
from core.constants.resources import RESOURCE_INFO
from .models import StudentRecord, Announcement, AnnouncementRead, Course, Enrollment
from django.shortcuts import get_object_or_404
from .forms import GradeUpdateForm, AnnouncementForm

@login_required
def dashboard_home(request):
    profile = request.user.profile
    role = profile.role.lower()

    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good Morning"
    elif hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    unread_announcements = Announcement.objects.exclude(
        announcementread__user=request.user,
        announcementread__is_read=True
    )

    pinned_urls = list(
        profile.pinned_resources.values_list("resource_id", flat=True)
    )

    resources = [
        {"id": rid, **data}
        for rid, data in RESOURCE_INFO.items()
        if role in data["roles"]
    ]

    return render(request, "dashboard/home.html", {
        "role": role,
        "greeting": greeting,
        "resources": resources,
        "pinned_urls": pinned_urls,
        "announcements": unread_announcements,
    })
        
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
   announcement = get_object_or_404(Announcement, id=announcement_id)

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

    enrollments = []
    if record:
        enrollments = record.enrollments.select_related("course", "course__professor").all()

    return render(request, "dashboard/degree_audit.html", {
        "record": record,
        "enrollments": enrollments,
    })

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

@login_required
def resource_unavailable(request, resource_id):
    resource = RESOURCE_INFO.get(resource_id)

    resource_title = resource["title"] if resource else "This resource"

    return render(request, "dashboard/resource_unavailable.html", {
        "resource_title": resource_title,
    })

@login_required
def course_management_view(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": "student"}
    )

    if profile.role != "professor":
        return render(request, "dashboard/access_denied.html")

    courses = Course.objects.filter(professor=request.user).order_by("course_code")

    return render(request, "dashboard/course_management.html", {
        "courses": courses
    })


@login_required
def course_detail_view(request, course_id):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": "student"}
    )

    if profile.role != "professor":
        return render(request, "dashboard/access_denied.html")

    course = get_object_or_404(Course, id=course_id, professor=request.user)
    enrollments = Enrollment.objects.filter(course=course).select_related("student").order_by("student__full_name")

    return render(request, "dashboard/course_detail.html", {
        "course": course,
        "enrollments": enrollments
    })


@login_required
def update_grade_view(request, enrollment_id):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": "student"}
    )

    if profile.role != "professor":
        return render(request, "dashboard/access_denied.html")

    enrollment = get_object_or_404(
        Enrollment.objects.select_related("course"),
        id=enrollment_id,
        course__professor=request.user
    )

    if request.method == "POST":
        form = GradeUpdateForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            messages.success(request, "Grade updated successfully.")
            return redirect("course_detail", course_id=enrollment.course.id)
    else:
        form = GradeUpdateForm(instance=enrollment)

    return render(request, "dashboard/update_grade.html", {
        "form": form,
        "enrollment": enrollment
    })

# This method will allow student to view the available courses for particular samester
@login_required
def available_courses_view(request):
    student_record = StudentRecord.objects.filter(user=request.user).first()

    if not student_record:
        return render(request, "dashboard/access_denied.html")

    courses = Course.objects.all().order_by("course_code", "section")

    enrolled_course_ids = Enrollment.objects.filter(
        student=student_record
    ).values_list("course_id", flat=True)

    return render(request, "dashboard/available_courses.html", {
        "courses": courses,
        "enrolled_course_ids": enrolled_course_ids,
    })

# This method will allow student to view the enrolled courses
# If student is trying to enroll same course again it will give an error
def enroll_course_view(request, course_id):
    student_record = StudentRecord.objects.filter(user=request.user).first()

    if not student_record:
        return render(request, "dashboard/access_denied.html")

    course = get_object_or_404(Course, id=course_id)

    enrollment, created = Enrollment.objects.get_or_create(
        course=course,
        student=student_record,
        defaults={"grade": ""}
    )

    if created:
        messages.success(request, f"You enrolled in {course.course_code} successfully.")
    else:
        messages.warning(request, f"You are already enrolled in {course.course_code}.")

    return redirect("available_courses")

# This method will allows student to withdrow the registered classes 
@login_required
def withdraw_registered_course(request, course_id):
    student_record = StudentRecord.objects.filter(user=request.user).first()

    if not student_record:
        return render(request, "dashboard/access_denied.html")

    course = get_object_or_404(Course, id=course_id)

    enrollment = Enrollment.objects.filter(
        course=course,
        student=student_record
    ).first()

    if enrollment:
        enrollment.delete()
        messages.success(request, f"You withdrew from {course.course_code} successfully.")
    else:
        messages.warning(request, f"You are not enrolled in {course.course_code}.")

    return redirect("available_courses")
