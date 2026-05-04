from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.core.exceptions import ValidationError

from core.models import Institution, InstitutionMembership


class StudentRecord(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="student_records",
        null=True,
        blank=True,
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name="student_records",
    )
    student_id = models.IntegerField()
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["institution", "student_id"],
                name="unique_student_id_per_institution",
            )
        ]

    def __str__(self):
        return f"{self.full_name} ({self.student_id}) - {self.institution.code}"


class ProfessorRecord(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="professor_records",
        null=True,
        blank=True,
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name="professor_records",
    )
    professor_id = models.IntegerField()
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["institution", "professor_id"],
                name="unique_professor_id_per_institution",
            )
        ]

    def __str__(self):
        return f"{self.full_name} ({self.professor_id}) - {self.institution.code}"


class Course(models.Model):
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name="courses",
    )
    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=100)
    semester = models.CharField(max_length=50, blank=True, default="")
    section = models.CharField(max_length=10)
    credit_hours = models.PositiveSmallIntegerField(default=3)
    professor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courses_taught",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["institution", "course_code", "semester", "section"],
                name="unique_course_offering_per_institution",
            )
        ]

    def clean(self):
        if self.institution_id and self.professor_id:
            is_valid_professor = InstitutionMembership.objects.filter(
                user=self.professor,
                institution=self.institution,
                role=InstitutionMembership.PROFESSOR,
            ).exists()

            if not is_valid_professor:
                raise ValidationError({
                    "professor": "Selected professor must be a professor at this institution."
                })

    def __str__(self):
        return f"{self.institution.code} - {self.course_code} - {self.course_name} ({self.semester}, Section {self.section})"


class Enrollment(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    student = models.ForeignKey(
        StudentRecord,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    grade = models.CharField(max_length=10, blank=True, default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course", "student"],
                name="unique_student_course_enrollment",
            )
        ]

    def clean(self):
        if self.course_id and self.student_id:
            if self.course.institution_id != self.student.institution_id:
                raise ValidationError("Student and course must belong to the same institution.")

    def __str__(self):
        return f"{self.student.full_name} - {self.course.course_code}"


class Announcement(models.Model):
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name="announcements",
    )
    professor = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="announcements",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.course_id and self.institution_id:
            if self.course.institution_id != self.institution_id:
                raise ValidationError("Announcement course must belong to the selected institution.")

    def __str__(self):
        return self.title


class AnnouncementRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "announcement"],
                name="unique_announcement_read_status",
            )
        ]