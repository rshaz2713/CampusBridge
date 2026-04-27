from django import forms
from dashboard.models import Enrollment

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
