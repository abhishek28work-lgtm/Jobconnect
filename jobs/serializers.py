from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job

        fields = [
            'id',
            'title',
            'description',
            'skills_required',
            'location',
            'salary',
            'job_type',
            'created_at',
        ]