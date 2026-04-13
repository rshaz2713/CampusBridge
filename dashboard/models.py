from django.db import models
from django.contrib.auth.models import User


# STUDENT TABLE
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


# PROFESSOR TABLE
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



# COURSE TABLE
class Course(models.Model):
    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=100)

    professor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courses_taught"
    )

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"
    
# Professor Announcement Table
class Announcement(models.Model):
    professor = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#This model tracks which announcements have been read by which students
class AnnouncementRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'announcement')