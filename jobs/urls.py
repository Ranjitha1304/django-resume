from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('job/<slug:slug>/', views.job_detail, name='job_detail'),
    path('job/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('employer/jobs/', views.employer_jobs, name='employer_jobs'),
    path('employer/jobs/create/', views.create_job, name='create_job'),
    path('employer/jobs/<int:job_id>/applicants/', views.applicants_list, name='applicants_list'),
    path('application/<int:app_id>/shortlist/', views.shortlist_applicant, name='shortlist_applicant'),
    path('application/<int:app_id>/schedule/', views.schedule_interview, name='schedule_interview'),
]
