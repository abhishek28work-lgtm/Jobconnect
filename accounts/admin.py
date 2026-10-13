from django.contrib import admin

# Register your models here.

from .models import JobSeekerProfile, EmployerProfile


admin.site.register(JobSeekerProfile)
admin.site.register(EmployerProfile)