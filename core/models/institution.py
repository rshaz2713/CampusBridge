from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Institution(models.Model):
    name = models.CharField(max_length=255)
    code = models.SlugField(max_length=50, unique=True)
    primary_color = models.CharField(max_length=20, default="#0d6efd")

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

@receiver(post_save, sender=InstitutionMembership)
def create_institution_record(sender, instance, created, **kwargs):
    if not created:
        return

    from dashboard.models import StudentRecord, ProfessorRecord

    user = instance.user
    institution = instance.institution
    full_name = f"{user.first_name} {user.last_name}".strip() or user.username
    email = user.email or ""

    if instance.role == InstitutionMembership.STUDENT:
        StudentRecord.objects.get_or_create(
            user=user,
            institution=institution,
            defaults={
                "student_id": user.id + 1000 + institution.id,
                "full_name": full_name,
                "email": email,
            },
        )

    elif instance.role == InstitutionMembership.PROFESSOR:
        ProfessorRecord.objects.get_or_create(
            user=user,
            institution=institution,
            defaults={
                "professor_id": user.id + 5000 + institution.id,
                "full_name": full_name,
                "email": email,
            },
        )