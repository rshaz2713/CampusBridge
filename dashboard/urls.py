from django.urls import path
from .views import (dashboard_home, degree_audit_view, professor_search_view, professor_student_degree_audit_view, 
                    announcement_list_view, announcement_detail_view, delete_announcement_view,
                    course_management_view, course_detail_view, update_grade_view, available_courses_view, enroll_course_view, withdraw_registered_course,
                    resource_unavailable)

urlpatterns = [
    path("", dashboard_home, name="dashboard_home"),
    path("degree-audit/", degree_audit_view, name="degree_audit"),
    path("search-student/", professor_search_view, name="professor_search"),
    path("student/<int:student_id>/degree-audit/", professor_student_degree_audit_view, name="professor_student_degree_audit"),

    path("announcements/", announcement_list_view, name="announcement_list"),
    path("announcements/<int:announcement_id>/", announcement_detail_view, name="announcement_details"),
    path("announcements/delete/<int:announcement_id>/", delete_announcement_view, name="delete_announcement"),

    path("courses/", course_management_view, name="course_management"),
    path("courses/<int:course_id>/", course_detail_view, name="course_detail"),
    path("enrollments/<int:enrollment_id>/grade/", update_grade_view, name="update_grade"),

    path("available-courses/", available_courses_view, name="available_courses"),
    path("enroll-course/<int:course_id>/", enroll_course_view, name="enroll_course"),
    path("withdraw-course/<int:course_id>/", withdraw_registered_course, name="withdraw_course"),

    path("resource-unavailable/<str:resource_id>/", resource_unavailable, name="resource_unavailable"),
]
