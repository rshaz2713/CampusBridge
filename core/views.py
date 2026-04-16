from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms
from .models import Profile
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

    def generate_university_email(self, first_name, last_name):
        base_email = f"{last_name.lower()}{first_name[0].lower()}@university.com"
        email = base_email
        counter = 1

        # make sure email stays unique
        from django.contrib.auth.models import User
        while User.objects.filter(email=email).exists():
            email = f"{last_name.lower()}{first_name[0].lower()}{counter}@university.com"
            counter += 1

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        first_name = self.cleaned_data["first_name"].strip()
        last_name = self.cleaned_data["last_name"].strip()
        role = self.cleaned_data["role"]

        user.first_name = first_name
        user.last_name = last_name
        user.email = self.generate_university_email(first_name, last_name)

        if commit:
            user.save()

            user.profile.role = role
            user.profile.save()

            full_name = f"{first_name} {last_name}"
            email = user.email

            if role == "student":
                student_count = StudentRecord.objects.count() + 1
                student_id = 1000 + student_count

                StudentRecord.objects.create(
                    user=user,
                    student_id=student_id,
                    full_name=full_name,
                    email=email
                )

            elif role == "professor":
                professor_count = ProfessorRecord.objects.count() + 1
                professor_id = 1000 + professor_count

                ProfessorRecord.objects.create(
                    user=user,
                    professor_id=professor_id,
                    full_name=full_name,
                    email=email
                )

        return user


def home(request):
    return render(request, "core/home.html")


def register_view(request):
    if request.method == "POST":
        form = CampusBridgeRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard_home")
    else:
        form = CampusBridgeRegisterForm()

    return render(request, "registration/register.html", {"form": form})