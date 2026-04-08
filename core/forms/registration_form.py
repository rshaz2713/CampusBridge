from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import Profile

class CampusBridgeRegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control custom-input"})
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control custom-input", "placeholder": "Enter first name"})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control custom-input", "placeholder": "Enter last name"})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control custom-input", "placeholder": "Enter username"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control custom-input", "placeholder": "Enter password"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control custom-input", "placeholder": "Confirm password"})
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
            role = self.cleaned_data["role"]
            user.profile.role = role
            user.profile.save()

        return user