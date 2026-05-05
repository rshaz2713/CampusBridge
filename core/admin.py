from django.contrib import admin
from .models import Profile, PinnedResource, Institution, InstitutionMembership


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "primary_color")
    search_fields = ("name", "code")


@admin.register(InstitutionMembership)
class InstitutionMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "institution", "role")
    list_filter = ("institution", "role")
    search_fields = ("user__username", "institution__name", "institution__code")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    list_filter = ("role",)
    search_fields = ("user__username",)


@admin.register(PinnedResource)
class PinnedResourceAdmin(admin.ModelAdmin):
    list_display = ("profile", "title", "url", "pinned_at")
    list_filter = ("pinned_at",)
    search_fields = ("title", "profile__user__username")