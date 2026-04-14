from django.contrib import admin
from .models import Profile, PinnedResource

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    list_filter = ("role",)
    search_fields = ("user__username",)

@admin.register(PinnedResource)  # ✅ Register PinnedResource
class PinnedResourceAdmin(admin.ModelAdmin):
    list_display = ['profile', 'title', 'url', 'pinned_at']
    list_filter = ['pinned_at']
    search_fields = ['title', 'profile__user__username']