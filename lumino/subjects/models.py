from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Subject(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_subjects'
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='subjects.Enrollment', related_name='students_subjects'
    )

    def __str__(self):
        return f'{self.code} - {self.name}'


class Lesson(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.CASCADE, related_name='lessons'
    )

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrolled'
    )
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.CASCADE, related_name='enrollment'
    )
    enrolled_at = models.DateField(auto_now_add=True)
    mark = models.PositiveSmallIntegerField(
        blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        ordering = ['student__last_name', 'student__first_name']

    def __str__(self):
        return f'{self.student} ({self.subject}) {self.mark}'
