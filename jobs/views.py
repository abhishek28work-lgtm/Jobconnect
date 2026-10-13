from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from applications.models import Application

from django.core.paginator import Paginator

from .serializers import JobSerializer

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from accounts.models import EmployerProfile, JobSeekerProfile
from .forms import JobForm
from .models import Job


# =========================
# POST JOB
# =========================

@login_required
def post_job(request):

    # Only employers can post jobs
    if not EmployerProfile.objects.filter(
        user=request.user
    ).exists():

        return redirect('home')

    employer = EmployerProfile.objects.get(
        user=request.user
    )

    if request.method == 'POST':

        form = JobForm(request.POST)

        if form.is_valid():

            job = form.save(commit=False)

            job.employer = employer

            job.save()

            return redirect('employer_dashboard')

    else:

        form = JobForm()

    return render(
        request,
        'post_job.html',
        {
            'form': form
        }
    )

# =========================
# EMPLOYER JOBS
# =========================

@login_required
def employer_jobs(request):

    if not EmployerProfile.objects.filter(
        user=request.user
    ).exists():

        return redirect('home')

    employer = EmployerProfile.objects.get(
        user=request.user
    )

    jobs = Job.objects.filter(
        employer=employer
    ).order_by('-created_at')

    return render(
        request,
        'employer_jobs.html',
        {
            'jobs': jobs
        }
    )



# =========================
# AVAILABLE JOBS
# =========================
@login_required
def available_jobs(request):

    # Only job seekers can access this page
    if not JobSeekerProfile.objects.filter(
        user=request.user
    ).exists():
        return redirect('home')

    # Read search and filter values
    search = request.GET.get('search', '').strip()
    location = request.GET.get('location', '').strip()
    job_type = request.GET.get('job_type', '').strip()

    # Get all jobs, newest first
    jobs = Job.objects.all().order_by('-created_at')

    # Search by title or required skills
    if search:
        jobs = jobs.filter(
            Q(title__icontains=search) |
            Q(skills_required__icontains=search)
        )

    # Filter by location
    if location:
        jobs = jobs.filter(
            location__icontains=location
        )

    # Filter by job type
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    # Pagination: 6 jobs per page
    paginator = Paginator(jobs, 6)
    page_number = request.GET.get('page')
    jobs_page = paginator.get_page(page_number)

    # Send data to the template
    context = {
        'jobs': jobs_page,
        'page_obj': jobs_page,
        'search': search,
        'location': location,
        'job_type': job_type,
    }

    return render(
        request,
        'available_jobs.html',
        context
    )







# =========================
# JOB DETAILS
# =========================


@login_required
def job_detail(request, job_id):

    # Only job seekers can view job details
    if not JobSeekerProfile.objects.filter(
        user=request.user
    ).exists():
        return redirect('home')

    job = get_object_or_404(Job, id=job_id)

    # Get the current job seeker's profile
    job_seeker = JobSeekerProfile.objects.get(
        user=request.user
    )

    # Check whether the job seeker has already applied
    has_applied = Application.objects.filter(
        job=job,
        job_seeker=job_seeker
    ).exists()

    return render(
        request,
        'job_detail.html',
        {
            'job': job,
            'has_applied': has_applied,
        }
    )




# =========================
# EDIT JOB
# =========================

@login_required
def edit_job(request, job_id):

    if not EmployerProfile.objects.filter(
        user=request.user
    ).exists():

        return redirect('home')

    employer = EmployerProfile.objects.get(
        user=request.user
    )

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=employer
    )

    if request.method == 'POST':

        form = JobForm(
            request.POST,
            instance=job
        )

        if form.is_valid():

            form.save()

            return redirect('employer_dashboard')

    else:

        form = JobForm(
            instance=job
        )

    return render(
        request,
        'edit_job.html',
        {
            'form': form,
            'job': job
        }
    )


# =========================
# DELETE JOB
# =========================

@login_required
def delete_job(request, job_id):

    if not EmployerProfile.objects.filter(
        user=request.user
    ).exists():

        return redirect('home')

    employer = EmployerProfile.objects.get(
        user=request.user
    )

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=employer
    )

    if request.method == 'POST':

        job.delete()

        return redirect('employer_dashboard')

    return render(
        request,
        'delete_job.html',
        {
            'job': job
        }
    )

# =========================
# JOB API
# =========================

@api_view(['GET'])
def job_api(request):

    jobs = Job.objects.all().order_by('-created_at')

    serializer = JobSerializer(
        jobs,
        many=True
    )

    return Response(
        serializer.data
    )
# =========================
# SINGLE JOB API
# =========================

@api_view(['GET'])
def single_job_api(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id
    )

    serializer = JobSerializer(job)

    return Response(
        serializer.data
    )




# =========================
# CREATE JOB API
# =========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_job_api(request):
   

    if not EmployerProfile.objects.filter(
        user=request.user
    ).exists():

        return Response(
            {'error': 'Only employers can create jobs'},
            status=403
        )

    employer = EmployerProfile.objects.get(
        user=request.user
    )

    serializer = JobSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save(
            employer=employer
        )

        return Response(
            serializer.data,
            status=201
        )

    return Response(
        serializer.errors,
        status=400
    )

# =========================
# UPDATE JOB API
# =========================

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_job_api(request, job_id):


   

    if not EmployerProfile.objects.filter(
        user=request.user
    ).exists():

        return Response(
            {'error': 'Only employers can update jobs'},
            status=403
        )

    employer = EmployerProfile.objects.get(
        user=request.user
    )

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=employer
    )

    serializer = JobSerializer(
        job,
        data=request.data
    )

    if serializer.is_valid():

        serializer.save(
            employer=employer
        )

        return Response(
            serializer.data,
            status=200
        )

    return Response(
        serializer.errors,
        status=400
    )

# =========================
# DELETE JOB API
# =========================

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_job_api(request, job_id):
    if not EmployerProfile.objects.filter(
        user=request.user
    ).exists():

        return Response(
            {'error': 'Only employers can delete jobs'},
            status=403
        )

    employer = EmployerProfile.objects.get(
        user=request.user
    )

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=employer
    )

    job.delete()

    return Response(
        {'message': 'Job deleted successfully'},
        status=200
    )

# =========================
# DELETE JOB API
# =========================

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_job_api(request, job_id):

    if not EmployerProfile.objects.filter(
        user=request.user
    ).exists():

        return Response(
            {'error': 'Only employers can delete jobs'},
            status=403
        )

    employer = EmployerProfile.objects.get(
        user=request.user
    )

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=employer
    )

    job.delete()

    return Response(
        {'message': 'Job deleted successfully'},
        status=200
    )