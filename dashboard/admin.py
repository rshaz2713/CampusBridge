from django.contrib import admin
from django.contrib.auth.models import User

from core.models import InstitutionMembership
from .models import Announcement, AnnouncementRead, Course, Enrollment, ProfessorRecord, StudentRecord

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "course_code",
        "course_name",
        "institution",
        "semester",
        "section",
        "credit_hours",
        "professor",
    )
    list_filter = ("institution", "semester")
    search_fields = (
        "course_code",
        "course_name",
        "professor__username",
        "institution__name",
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "professor":
            kwargs["queryset"] = User.objects.filter(
                institution_memberships__role=InstitutionMembership.PROFESSOR
            ).distinct().order_by("username")

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(StudentRecord)
class StudentRecordAdmin(admin.ModelAdmin):
    list_display = ("full_name", "student_id", "email", "institution", "user")
    list_filter = ("institution",)
    search_fields = ("full_name", "student_id", "email", "user__username")


@admin.register(ProfessorRecord)
class ProfessorRecordAdmin(admin.ModelAdmin):
    list_display = ("full_name", "professor_id", "email", "institution", "user")
    list_filter = ("institution",)
    search_fields = ("full_name", "professor_id", "email", "user__username")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "grade")
    list_filter = ("course__institution", "course__semester")
    search_fields = (
        "student__full_name",
        "student__student_id",
        "course__course_code",
        "course__course_name",
    )


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "institution", "professor", "course", "created_at")
    list_filter = ("institution", "created_at")
    search_fields = ("title", "message", "professor__username")


@admin.register(AnnouncementRead)
class AnnouncementReadAdmin(admin.ModelAdmin):
    list_display = ("user", "announcement", "is_read")
    list_filter = ("is_read", "announcement__institution")