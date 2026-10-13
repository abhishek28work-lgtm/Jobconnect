from django.db import models
from accounts.models import EmployerProfile


class Job(models.Model):

    JOB_TYPE_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
    ]

    employer = models.ForeignKey(
        EmployerProfile,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    skills_required = models.CharField(
        max_length=300
    )

    location = models.CharField(
        max_length=200
    )

    salary = models.CharField(
        max_length=100,
        blank=True
    )

    job_type = models.CharField(
        max_length=50,
        choices=JOB_TYPE_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title