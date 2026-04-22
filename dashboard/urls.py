from django.urls import path
from .views import dashboard_home, degree_audit_view, professor_search_view, create_announcement_view, announcement_list_view, announcement_detail_view, resource_unavailable

urlpatterns = [
    path("", dashboard_home, name="dashboard_home"),
    path("degree-audit/", degree_audit_view, name="degree_audit"),
    path("search-student/", professor_search_view, name="professor_search"),
    path("create-announcement/", create_announcement_view, name="create_announcement"),
    path("announcements/", announcement_list_view, name="professor_announcement"),
    path("announcements/<int:announcement_id>/", announcement_detail_view, name="announcement_details"),
    path("resource-unavailable/<str:resource_id>/", resource_unavailable, name="resource_unavailable"),
]
