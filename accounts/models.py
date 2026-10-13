
from django.db import models
from django.contrib.auth.models import User


class JobSeekerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(max_length=15)

    skills = models.TextField()

    education = models.CharField(max_length=200)

    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username


class EmployerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    company_name = models.CharField(max_length=200)

    company_description = models.TextField()

    location = models.CharField(max_length=200)

    def __str__(self):
        return self.company_name


