from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ApplicationSerializer

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Application
from jobs.models import Job
from accounts.models import JobSeekerProfile, EmployerProfile


@login_required
def apply_job(request, job_id):

    # Only Job Seekers can apply
    if not JobSeekerProfile.objects.filter(
        user=request.user
    ).exists():

        return redirect('home')

    job_seeker = JobSeekerProfile.objects.get(
        user=request.user
    )

    job = get_object_or_404(
        Job,
        id=job_id
    )

    # Prevent duplicate application
    if Application.objects.filter(
        job=job,
        job_seeker=job_seeker
    ).exists():

        return redirect(
            'job_detail',
            job_id=job.id
        )

    Application.objects.create(
        job=job,
        job_seeker=job_seeker
    )

    return redirect(
        'job_detail',
        job_id=job.id
    )



@login_required
def my_applications(request):
    if not JobSeekerProfile.objects.filter(user=request.user).exists():
        return redirect('home')

    job_seeker = JobSeekerProfile.objects.get(user=request.user)

    applications = Application.objects.filter(
        job_seeker=job_seeker
    ).select_related(
        'job',
        'job__employer'
    ).order_by('-applied_at')

    return render(
        request,
        'my_applications.html',
        {'applications': applications}
    )



@login_required
def employer_applications(request):

    employer = EmployerProfile.objects.filter(
        user=request.user
    ).first()

    if employer is None:
        return redirect('home')

    applications = Application.objects.filter(
        job__employer=employer
    ).select_related(
        'job',
        'job_seeker',
        'job_seeker__user'
    ).order_by('-applied_at')

    return render(
        request,
        'employer_applications.html',
        {
            'applications': applications
        }
    )



@login_required
def accept_application(request, application_id):
    application = Application.objects.get(id=application_id)

    if application.job.employer.user != request.user:
        return redirect('home')

    application.status = 'Accepted'
    application.save()

    return redirect('employer_applications')


@login_required
def reject_application(request, application_id):
    application = Application.objects.get(id=application_id)

    if application.job.employer.user != request.user:
        return redirect('home')

    application.status = 'Rejected'
    application.save()

    return redirect('employer_applications')

# =========================
# APPLY FOR JOB API
# =========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_job_api(request, job_id):

    if not JobSeekerProfile.objects.filter(
        user=request.user
    ).exists():

        return Response(
            {'error': 'Only job seekers can apply for jobs'},
            status=403
        )

    job_seeker = JobSeekerProfile.objects.get(
        user=request.user
    )

    job = get_object_or_404(
        Job,
        id=job_id
    )

    if Application.objects.filter(
        job=job,
        job_seeker=job_seeker
    ).exists():

        return Response(
            {'error': 'You have already applied for this job'},
            status=400
        )

    application = Application.objects.create(
        job=job,
        job_seeker=job_seeker
    )

    serializer = ApplicationSerializer(
        application
    )

    return Response(
        serializer.data,
        status=201
    )

# =========================
# MY APPLICATIONS API
# =========================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_applications_api(request):

    if not JobSeekerProfile.objects.filter(
        user=request.user
    ).exists():

        return Response(
            {'error': 'Only job seekers can view applications'},
            status=403
        )

    job_seeker = JobSeekerProfile.objects.get(
        user=request.user
    )

    applications = Application.objects.filter(
        job_seeker=job_seeker
    )

    serializer = ApplicationSerializer(
        applications,
        many=True
    )

    return Response(
        serializer.data,
        status=200
    )

# =========================
# EMPLOYER APPLICATIONS API
# =========================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employer_applications_api(request):

    if not EmployerProfile.objects.filter(
        user=request.user
    ).exists():

        return Response(
            {'error': 'Only employers can view applications'},
            status=403
        )

    employer = EmployerProfile.objects.get(
        user=request.user
    )

    applications = Application.objects.filter(
        job__employer=employer
    )

    serializer = ApplicationSerializer(
        applications,
        many=True
    )

    return Response(
        serializer.data,
        status=200
    )

# =========================
# ACCEPT APPLICATION API
# =========================

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def accept_application_api(request, application_id):

    if not EmployerProfile.objects.filter(
        user=request.user
    ).exists():

        return Response(
            {'error': 'Only employers can accept applications'},
            status=403
        )

    employer = EmployerProfile.objects.get(
        user=request.user
    )

    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer=employer
    )

    application.status = 'Accepted'
    application.save()

    serializer = ApplicationSerializer(
        application
    )

    return Response(
        serializer.data,
        status=200
    )


# =========================
# REJECT APPLICATION API
# =========================

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def reject_application_api(request, application_id):

    if not EmployerProfile.objects.filter(
        user=request.user
    ).exists():

        return Response(
            {'error': 'Only employers can reject applications'},
            status=403
        )

    employer = EmployerProfile.objects.get(
        user=request.user
    )

    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer=employer
    )

    application.status = 'Rejected'
    application.save()

    serializer = ApplicationSerializer(
        application
    )

    return Response(
        serializer.data,
        status=200
    )