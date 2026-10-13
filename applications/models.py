from django.db import models
from jobs.models import Job
from accounts.models import JobSeekerProfile


class Application(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    job_seeker = models.ForeignKey(
        JobSeekerProfile,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            'job',
            'job_seeker'
        )

    def __str__(self):
        return (
            f"{self.job.title} - "
            f"{self.job_seeker.user.username}"
        )