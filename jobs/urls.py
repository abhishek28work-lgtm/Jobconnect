from django.urls import path

from .views import (
    post_job,
    employer_jobs,
    available_jobs,
    job_detail,
    edit_job,
    delete_job,
    job_api,
    single_job_api,
     create_job_api,
       update_job_api,
       delete_job_api
)

urlpatterns = [
    path('post-job/', post_job, name='post_job'),
    path('employer-jobs/', employer_jobs, name='employer_jobs'),
    path('available-jobs/', available_jobs, name='available_jobs'),
    path('job/<int:job_id>/', job_detail, name='job_detail'),
    path('edit-job/<int:job_id>/', edit_job, name='edit_job'),
    path('delete-job/<int:job_id>/', delete_job, name='delete_job'),

    path('api/jobs/', job_api, name='job_api'),

    path(
        'api/jobs/<int:job_id>/',
        single_job_api,
        name='single_job_api'
    ),
    path(
    'api/jobs/create/',
    create_job_api,
    name='create_job_api'
),
path(
    'api/jobs/<int:job_id>/update/',
    update_job_api,
    name='update_job_api'
),
path(
    'api/jobs/<int:job_id>/delete/',
    delete_job_api,
    name='delete_job_api'
),
]