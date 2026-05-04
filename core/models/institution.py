from django.contrib.auth.models import User
from django.db import models


class Institution(models.Model):
    name = models.CharField(max_length=255)
    code = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class InstitutionMembership(models.Model):
    STUDENT = "student"
    PROFESSOR = "professor"

    ROLE_CHOICES = [
        (STUDENT, "Student"),
        (PROFESSOR, "Professor"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="institution_memberships",
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "institution", "role"],
                name="unique_user_institution_role",
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.institution.code} - {self.role}"