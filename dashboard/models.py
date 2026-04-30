from django.db import models
from django.contrib.auth.models import User

# Student table
class StudentRecord(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_record",
        null=True,
        blank=True
    )
    student_id = models.IntegerField(unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, default="")

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"

# Professor table
class ProfessorRecord(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="professor_record",
        null=True,
        blank=True
    )

    professor_id = models.IntegerField(unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, default="")

    def __str__(self):
        return f"{self.full_name} ({self.professor_id})"
    
# Announcements
class Announcement(models.Model):
    professor = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Tracks which announcements have been read by which students
class AnnouncementRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'announcement')

# Course table
class Course(models.Model):
    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=100)
    semester = models.CharField(max_length=50, blank=True, default="")
    section = models.CharField(max_length=10)
    professor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courses_taught"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course_code", "semester", "section"], name="unique_course_offering"
            )
        ]

    def __str__(self):
        return f"{self.course_code} - {self.course_name} ({self.semester}, Section {self.section})"

# Enrollment table
class Enrollment(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    student = models.ForeignKey(
        StudentRecord,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    grade = models.CharField(max_length=10, blank=True, default="")

    class Meta:
        unique_together = ("course", "student")

    def __str__(self):
        return f"{self.student.full_name} - {self.course.course_code}"
