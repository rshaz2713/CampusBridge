from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import Profile
from dashboard.models import StudentRecord, ProfessorRecord

class CampusBridgeRegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-control custom-input"
        })
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control custom-input",
            "placeholder": "Enter first name"
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control custom-input",
            "placeholder": "Enter last name"
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control custom-input",
            "placeholder": "Enter email"
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control custom-input",
            "placeholder": "Enter username"
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control custom-input",
            "placeholder": "Enter password"
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control custom-input",
            "placeholder": "Confirm password"
        })
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

            role = self.cleaned_data["role"]
            user.profile.role = role
            user.profile.save()

            full_name = f"{user.first_name} {user.last_name}".strip() or user.username
            email = user.email or ""

            if role == "student":
                StudentRecord.objects.get_or_create(
                    user=user,
                    defaults={
                        "student_id": user.id + 1000,
                        "full_name": full_name,
                        "email": email,
                    }
                )
            elif role == "professor":
                ProfessorRecord.objects.get_or_create(
                    user=user,
                    defaults={
                        "professor_id": user.id + 5000,
                        "full_name": full_name,
                        "email": email,
                    }
                )

        return user