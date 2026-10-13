from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm
from .models import JobSeekerProfile, EmployerProfile

from django.views.decorators.csrf import ensure_csrf_cookie


# =========================
# HOME
# =========================



@ensure_csrf_cookie
def home(request):
    return render(request, 'home.html')


# =========================
# REGISTER
# =========================

def register(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']

            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Create Job Seeker profile
            if role == 'jobseeker':

                JobSeekerProfile.objects.create(
                    user=user,
                    phone='',
                    skills='',
                    education=''
                )

            # Create Employer profile
            elif role == 'employer':

                EmployerProfile.objects.create(
                    user=user,
                    company_name='',
                    company_description='',
                    location=''
                )

            # Login automatically
            login(request, user)

            messages.success(
                request,
                'Registration successful!'
            )

            # Redirect according to role
            if role == 'jobseeker':

                return redirect(
                    'jobseeker_dashboard'
                )

            elif role == 'employer':

                return redirect(
                    'employer_dashboard'
                )

    else:

        form = UserRegistrationForm()

    return render(
        request,
        'register.html',
        {
            'form': form
        }
    )


# =========================
# LOGIN
# =========================

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                'Login successful!'
            )

            # Job Seeker
            if JobSeekerProfile.objects.filter(
                user=user
            ).exists():

                return redirect(
                    'jobseeker_dashboard'
                )

            # Employer
            elif EmployerProfile.objects.filter(
                user=user
            ).exists():

                return redirect(
                    'employer_dashboard'
                )

            return redirect('home')

        else:

            return render(
                request,
                'login.html',
                {
                    'error': 'Invalid username or password.'
                }
            )

    return render(
        request,
        'login.html'
    )


# =========================
# LOGOUT
# =========================

def user_logout(request):

    logout(request)

    messages.success(
        request,
        'You have been logged out.'
    )

    return redirect('home')


# =========================
# JOB SEEKER DASHBOARD
# =========================

def jobseeker_dashboard(request):

    if not request.user.is_authenticated:

        return redirect('login')

    return render(
        request,
        'jobseeker_dashboard.html'
    )


# =========================
# EMPLOYER DASHBOARD
# =========================


@login_required
def employer_dashboard(request):

    if not EmployerProfile.objects.filter(
        user=request.user
    ).exists():
        return redirect('home')

    return render(
        request,
        'employer_dashboard.html'
    )

# =========================
# JOB SEEKER PROFILE
# =========================

@login_required
def jobseeker_profile(request):

    if not JobSeekerProfile.objects.filter(
        user=request.user
    ).exists():

        return redirect('home')

    profile = JobSeekerProfile.objects.get(
        user=request.user
    )

    if request.method == 'POST':

        profile.phone = request.POST.get('phone')
        profile.skills = request.POST.get('skills')
        profile.education = request.POST.get('education')

        if request.FILES.get('resume'):
            profile.resume = request.FILES.get('resume')

        profile.save()

        messages.success(
            request,
            'Profile updated successfully!'
        )

        return redirect('jobseeker_profile')

    return render(
        request,
        'jobseeker_profile.html',
        {
            'profile': profile
        }
    )

# =========================
# EMPLOYER PROFILE
# =========================

@login_required
def employer_profile(request):

    if not EmployerProfile.objects.filter(
        user=request.user
    ).exists():

        return redirect('home')

    profile = EmployerProfile.objects.get(
        user=request.user
    )

    if request.method == 'POST':

        profile.company_name = request.POST.get('company_name')
        profile.company_description = request.POST.get('company_description')
        profile.location = request.POST.get('location')

        profile.save()

        messages.success(
            request,
            'Company profile updated successfully!'
        )

        return redirect('employer_profile')

    return render(
        request,
        'employer_profile.html',
        {
            'profile': profile
        }
    )