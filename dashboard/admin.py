from django.contrib import admin
from .models import StudentRecord, ProfessorRecord, Course, Announcement

@admin.register(StudentRecord)
class StudentRecordAdmin(admin.ModelAdmin):
    list_display = ("full_name", "student_id", "email", "user")
    search_fields = ("full_name", "student_id", "email", "user__username")


@admin.register(ProfessorRecord)
class ProfessorRecordAdmin(admin.ModelAdmin):
    list_display = ("full_name", "professor_id", "email", "user")
    search_fields = ("full_name", "professor_id", "email", "user__username")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_code", "course_name", "professor")
    search_fields = ("course_code", "course_name", "professor__username")

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "professor", "created_at")
    search_fields = ("title", "message", "professor__username")
