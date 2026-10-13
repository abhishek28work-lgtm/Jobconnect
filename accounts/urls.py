from django.urls import path

from .views import (
    home,
    register,
    user_login,
    user_logout,
    jobseeker_dashboard,
    employer_dashboard,
    jobseeker_profile,
    employer_profile
)


urlpatterns = [

    path(
        '',
        home,
        name='home'
    ),

    path(
        'register/',
        register,
        name='register'
    ),

    path(
        'login/',
        user_login,
        name='login'
    ),

    path(
        'logout/',
        user_logout,
        name='logout'
    ),

    path(
        'jobseeker/dashboard/',
        jobseeker_dashboard,
        name='jobseeker_dashboard'
    ),

    path(
        'employer/dashboard/',
        employer_dashboard,
        name='employer_dashboard'
    ),

    path(
        'jobseeker/profile/',
        jobseeker_profile,
        name='jobseeker_profile'
    ),

    path(
        'employer/profile/',
        employer_profile,
        name='employer_profile'
    ),
]