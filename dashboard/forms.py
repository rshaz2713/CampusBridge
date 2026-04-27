from django import forms
from dashboard.models import Enrollment, Announcement

class GradeUpdateForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ["grade"]
        widgets = {
            "grade": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter grade"
            })
        }

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
