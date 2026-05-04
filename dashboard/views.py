from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.constants.resources import RESOURCE_INFO
from core.models import InstitutionMembership
from .forms import AnnouncementForm, GradeUpdateForm
from .models import Announcement, AnnouncementRead, Course, Enrollment, StudentRecord


def get_current_membership(request):
    if not request.user.is_authenticated:
        return None

    memberships = (
        InstitutionMembership.objects
        .filter(user=request.user)
        .select_related("institution")
    )

    current_membership_id = request.session.get("current_membership_id")
    membership = None

    if current_membership_id:
        membership = memberships.filter(id=current_membership_id).first()

    if membership is None:
        membership = memberships.first()
        if membership:
            request.session["current_membership_id"] = membership.id
            request.session["current_institution_id"] = membership.institution_id

    return membership


def require_membership(request):
    membership = get_current_membership(request)

    if not membership:
        return None, None

    return membership, membership.institution


@login_required
def switch_institution(request):
    if request.method == "POST":
        membership_id = request.POST.get("membership_id")

        membership = InstitutionMembership.objects.filter(
            id=membership_id,
            user=request.user,
        ).first()

        if membership:
            request.session["current_membership_id"] = membership.id
            request.session["current_institution_id"] = membership.institution_id

    return redirect(request.META.get("HTTP_REFERER", "dashboard_home"))


@login_required
def dashboard_home(request):
    membership, current_institution = require_membership(request)

    if not membership:
        return render(request, "dashboard/home.html", {
            "error": "No institution access has been assigned to your account."
        })

    role = membership.role

    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good Morning"
    elif hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    profile = request.user.profile

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
        "current_institution": current_institution,
    })


@login_required
def announcement_list_view(request):
    membership, current_institution = require_membership(request)

    if not membership:
        return render(request, "dashboard/access_denied.html")

    role = membership.role

    if request.method == "POST":
        if role != "professor":
            return render(request, "dashboard/access_denied.html")

        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.professor = request.user
            announcement.institution = current_institution
            announcement.save()
            return redirect("announcement_list")
    else:
        form = AnnouncementForm()

    if role == "professor":
        announcements = Announcement.objects.filter(
            institution=current_institution,
            professor=request.user,
        ).order_by("-created_at")
    else:
        announcements = Announcement.objects.filter(
            institution=current_institution
        ).order_by("-created_at")

    return render(request, "dashboard/announcement_list.html", {
        "announcements": announcements,
        "form": form,
        "role": role,
    })


@login_required
def announcement_detail_view(request, announcement_id):
    membership, current_institution = require_membership(request)

    if not membership:
        return render(request, "dashboard/access_denied.html")

    announcement = get_object_or_404(
        Announcement,
        id=announcement_id,
        institution=current_institution,
    )

    AnnouncementRead.objects.update_or_create(
        user=request.user,
        announcement=announcement,
        defaults={"is_read": True},
    )

    return render(request, "dashboard/announcement_details.html", {
        "announcement": announcement,
    })


@login_required
def delete_announcement_view(request, announcement_id):
    membership, current_institution = require_membership(request)

    if not membership or membership.role != "professor":
        return render(request, "dashboard/access_denied.html")

    announcement = get_object_or_404(
        Announcement,
        id=announcement_id,
        institution=current_institution,
        professor=request.user,
    )

    if request.method == "POST":
        announcement.delete()

    return redirect("announcement_list")


@login_required
def student_financial_docs_view(request):
    membership, current_institution = require_membership(request)

    if not membership or membership.role != "student":
        return render(request, "dashboard/access_denied.html")

    student_record = StudentRecord.objects.filter(
        user=request.user,
        institution=current_institution,
    ).first()

    if not student_record:
        return render(request, "dashboard/access_denied.html")

    enrollments = (
        Enrollment.objects
        .filter(
            student=student_record,
            course__institution=current_institution,
        )
        .select_related("course")
        .order_by("course__course_code")
    )

    total_credits = sum(enrollment.course.credit_hours for enrollment in enrollments)

    tuition_rate_per_credit = 650
    registration_fee = 58
    transportation_fee = 50
    full_time_tuition = 3499
    general_fee = 2358
    state_univ_fee = 528
    student_activity_fee = 100
    excess_credit_fee = 0

    if total_credits != 0:
        if total_credits < 12:
            estimated_balance = (
                total_credits * tuition_rate_per_credit
            ) + registration_fee + transportation_fee
        else:
            if total_credits > 18:
                excess_credit_fee = (total_credits - 18) * tuition_rate_per_credit

            estimated_balance = (
                full_time_tuition
                + general_fee
                + state_univ_fee
                + student_activity_fee
                + transportation_fee
                + excess_credit_fee
            )
    else:
        estimated_balance = 0

    return render(request, "dashboard/student_financial_docs.html", {
        "student_record": student_record,
        "enrollments": enrollments,
        "total_credits": total_credits,
        "tuition_rate_per_credit": tuition_rate_per_credit,
        "registration_fee": registration_fee,
        "transportation_fee": transportation_fee,
        "full_time_tuition": full_time_tuition,
        "general_fee": general_fee,
        "state_univ_fee": state_univ_fee,
        "student_activity_fee": student_activity_fee,
        "excess_credit_fee": excess_credit_fee,
        "estimated_balance": estimated_balance,
    })

@login_required
def employee_financial_docs_view(request):
    if request.user.profile.role != "professor":
        return render(request, "dashboard/access_denied.html")
    
    employee_name = request.user.get_full_name() or request.user.username
    employee_email = request.user.email

    pay_period = "Current Pay Period"
    timesheet_status = "Not submitted"
    latest_pay_statement = "Not available"
    w2_status = "Not available"

    return render(request, "dashboard/employee_financial_docs.html", {
        "employee_name": employee_name,
        "employee_email": employee_email,
        "timesheet_status": timesheet_status,
        "pay_period": pay_period,
        "latest_pay_statement": latest_pay_statement,
        "w2_status": w2_status,
    })

@login_required
def degree_audit_view(request):
    membership, current_institution = require_membership(request)

    if not membership or membership.role != "student":
        return render(request, "dashboard/access_denied.html")

    record = StudentRecord.objects.filter(
        user=request.user,
        institution=current_institution,
    ).first()

    enrollments = []
    if record:
        enrollments = (
            record.enrollments
            .filter(course__institution=current_institution)
            .select_related("course", "course__professor")
        )

    return render(request, "dashboard/degree_audit.html", {
        "record": record,
        "enrollments": enrollments,
    })


@login_required
def professor_search_view(request):
    membership, current_institution = require_membership(request)

    if not membership or membership.role != "professor":
        return render(request, "dashboard/access_denied.html")

    all_students = StudentRecord.objects.filter(
        institution=current_institution,
    ).order_by("student_id")

    return render(request, "dashboard/professor_search.html", {
        "all_students": all_students,
    })


@login_required
def professor_student_degree_audit_view(request, student_id):
    membership, current_institution = require_membership(request)

    if not membership or membership.role != "professor":
        return render(request, "dashboard/access_denied.html")

    record = get_object_or_404(
        StudentRecord,
        student_id=student_id,
        institution=current_institution,
    )

    student_first_name = record.full_name.split()[0] if record.full_name else "Student"

    enrollments = (
        record.enrollments
        .filter(course__institution=current_institution)
        .select_related("course", "course__professor")
    )

    return render(request, "dashboard/degree_audit.html", {
        "record": record,
        "enrollments": enrollments,
        "viewing_as_professor": True,
        "student_first_name": student_first_name,
    })


@login_required
def course_management_view(request):
    membership, current_institution = require_membership(request)

    if not membership or membership.role != "professor":
        return render(request, "dashboard/access_denied.html")

    courses = Course.objects.filter(
        institution=current_institution,
        professor=request.user,
    ).order_by("course_code")

    return render(request, "dashboard/course_management.html", {
        "courses": courses,
    })


@login_required
def course_detail_view(request, course_id):
    membership, current_institution = require_membership(request)

    if not membership or membership.role != "professor":
        return render(request, "dashboard/access_denied.html")

    course = get_object_or_404(
        Course,
        id=course_id,
        institution=current_institution,
        professor=request.user,
    )

    enrollments = (
        Enrollment.objects
        .filter(
            course=course,
            course__institution=current_institution,
        )
        .select_related("student")
        .order_by("student__full_name")
    )

    return render(request, "dashboard/course_detail.html", {
        "course": course,
        "enrollments": enrollments,
    })


@login_required
def update_grade_view(request, enrollment_id):
    membership, current_institution = require_membership(request)

    if not membership or membership.role != "professor":
        return render(request, "dashboard/access_denied.html")

    enrollment = get_object_or_404(
        Enrollment.objects.select_related("course"),
        id=enrollment_id,
        course__institution=current_institution,
        course__professor=request.user,
    )

    if request.method == "POST":
        form = GradeUpdateForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            messages.success(request, "Grade updated successfully.")

    return redirect("course_detail", course_id=enrollment.course.id)


@login_required
def available_courses_view(request):
    membership, current_institution = require_membership(request)

    if not membership or membership.role != "student":
        return render(request, "dashboard/access_denied.html")

    student_record = StudentRecord.objects.filter(
        user=request.user,
        institution=current_institution,
    ).first()

    if not student_record:
        return render(request, "dashboard/access_denied.html")

    courses = Course.objects.filter(
        institution=current_institution,
    ).order_by("course_code", "section")

    enrolled_course_ids = Enrollment.objects.filter(
        student=student_record,
        course__institution=current_institution,
    ).values_list("course_id", flat=True)

    return render(request, "dashboard/available_courses.html", {
        "courses": courses,
        "enrolled_course_ids": enrolled_course_ids,
    })


@login_required
def enroll_course_view(request, course_id):
    membership, current_institution = require_membership(request)

    if not membership or membership.role != "student":
        return render(request, "dashboard/access_denied.html")

    student_record = StudentRecord.objects.filter(
        user=request.user,
        institution=current_institution,
    ).first()

    if not student_record:
        return render(request, "dashboard/access_denied.html")

    course = get_object_or_404(
        Course,
        id=course_id,
        institution=current_institution,
    )

    enrollment, created = Enrollment.objects.get_or_create(
        course=course,
        student=student_record,
        defaults={"grade": ""},
    )

    if created:
        messages.success(request, f"You enrolled in {course.course_code} successfully.")
    else:
        messages.warning(request, f"You are already enrolled in {course.course_code}.")

    return redirect("available_courses")


@login_required
def withdraw_registered_course(request, course_id):
    membership, current_institution = require_membership(request)

    if not membership or membership.role != "student":
        return render(request, "dashboard/access_denied.html")

    student_record = StudentRecord.objects.filter(
        user=request.user,
        institution=current_institution,
    ).first()

    if not student_record:
        return render(request, "dashboard/access_denied.html")

    course = get_object_or_404(
        Course,
        id=course_id,
        institution=current_institution,
    )

    enrollment = Enrollment.objects.filter(
        course=course,
        student=student_record,
        course__institution=current_institution,
    ).first()

    if enrollment:
        enrollment.delete()
        messages.success(request, f"You withdrew from {course.course_code} successfully.")
    else:
        messages.warning(request, f"You are not enrolled in {course.course_code}.")

    return redirect("available_courses")


@login_required
def resource_unavailable(request, resource_id):
    resource = RESOURCE_INFO.get(resource_id)
    resource_title = resource["title"] if resource else "This resource"

    return render(request, "dashboard/resource_unavailable.html", {
        "resource_title": resource_title,
    })
