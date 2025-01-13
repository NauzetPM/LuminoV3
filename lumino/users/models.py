from django.conf import settings
from django.db import models


class Profile(models.Model):
    class Role(models.TextChoices):
        STUDENT = 'S', 'Student'
        TEACHER = 'T', 'Teacher'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    avatar = models.ImageField(
        blank=True, null=True, upload_to='avatars', default='avatars/noavatar.png'
    )
    role = models.CharField(max_length=1, choices=Role, default=Role.STUDENT)
    bio = models.TextField(blank=True)

    @classmethod
    def is_teacher(cls, user):
        return user.profile.role == Profile.Role.TEACHER

    def __str__(self):
        return self.user.username
