from django.urls import path

from .views import (
    apply_job,
    my_applications,
    employer_applications,
    accept_application,
    reject_application,
    apply_job_api,
    my_applications_api,
    employer_applications_api,
    accept_application_api,
    reject_application_api,
)


urlpatterns = [

    # =========================
    # NORMAL WEBSITE URLS
    # =========================

    path(
        'apply/<int:job_id>/',
        apply_job,
        name='apply_job'
    ),

    path(
        'my-applications/',
        my_applications,
        name='my_applications'
    ),

    path(
        'employer-applications/',
        employer_applications,
        name='employer_applications'
    ),

    path(
        'accept/<int:application_id>/',
        accept_application,
        name='accept_application'
    ),

    path(
        'reject/<int:application_id>/',
        reject_application,
        name='reject_application'
    ),


    # =========================
    # REST API URLS
    # =========================

    path(
        'api/apply/<int:job_id>/',
        apply_job_api,
        name='apply_job_api'
    ),

    path(
        'api/my-applications/',
        my_applications_api,
        name='my_applications_api'
    ),

    path(
        'api/employer-applications/',
        employer_applications_api,
        name='employer_applications_api'
    ),

    path(
        'api/accept/<int:application_id>/',
        accept_application_api,
        name='accept_application_api'
    ),
    path(
    'api/reject/<int:application_id>/',
    reject_application_api,
    name='reject_application_api'
),

]