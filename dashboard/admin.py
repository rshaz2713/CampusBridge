from django.contrib import admin
from .models import StudentRecord, ProfessorRecord, Course, Announcement, AnnouncementRead, Course, Enrollment

@admin.register(StudentRecord)
class StudentRecordAdmin(admin.ModelAdmin):
    list_display = ("full_name", "student_id", "email", "user")
    search_fields = ("full_name", "student_id", "email", "user__username")

@admin.register(ProfessorRecord)
class ProfessorRecordAdmin(admin.ModelAdmin):
    list_display = ("full_name", "professor_id", "email", "user")
    search_fields = ("full_name", "professor_id", "email", "user__username")

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "professor", "created_at")
    search_fields = ("title", "message", "professor__username")

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_code", "course_name", "semester", "section", "professor")
    search_fields = ("course_code", "course_name", "semester", "section", "professor__username")

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "grade")
    search_fields = ("student__full_name", "course__course_code", "course__course_name", "grade")

