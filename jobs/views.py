from django.shortcuts import render, get_object_or_404, redirect
from .models import Job, Application, Interview
from .forms import JobForm, ApplicationForm, InterviewForm
from django.contrib.auth.decorators import login_required
from accounts.models import EmployerProfile, JobSeekerProfile
from django.core.paginator import Paginator
from django.contrib import messages

def job_list(request):
    q = request.GET.get('q', '')
    jobs = Job.objects.filter(is_active=True)
    if q:
        jobs = jobs.filter(title__icontains=q)  # simple search
    paginator = Paginator(jobs.order_by('-created_at'), 10)
    page = request.GET.get('page')
    jobs_page = paginator.get_page(page)
    return render(request, 'jobs/job_list.html', {'jobs': jobs_page, 'q': q})

def job_detail(request, slug):
    job = get_object_or_404(Job, slug=slug)
    applied = False
    if request.user.is_authenticated and request.user.is_jobseeker:
        seeker = get_object_or_404(JobSeekerProfile, user=request.user)
        applied = Application.objects.filter(job=job, jobseeker=seeker).exists()
    return render(request, 'jobs/job_detail.html', {'job': job, 'applied': applied})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if not request.user.is_jobseeker:
        messages.error(request, 'Only jobseekers can apply to jobs.')
        return redirect('job_detail', slug=job.slug)
    seeker = get_object_or_404(JobSeekerProfile, user=request.user)
    if Application.objects.filter(job=job, jobseeker=seeker).exists():
        messages.info(request, 'You have already applied to this job.')
        return redirect('job_detail', slug=job.slug)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.jobseeker = seeker
            # if no resume uploaded, copy from profile resume
            if not app.resume and seeker.resume:
                app.resume = seeker.resume
            app.save()
            messages.success(request, 'Application submitted successfully.')
            return redirect('dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})

@login_required
def employer_jobs(request):
    if not request.user.is_employer:
        messages.error(request, 'Access denied.')
        return redirect('job_list')
    profile = get_object_or_404(EmployerProfile, user=request.user)
    jobs = Job.objects.filter(employer=profile).order_by('-created_at')
    return render(request, 'jobs/employer_jobs.html', {'jobs': jobs})

@login_required
def create_job(request):
    if not request.user.is_employer:
        messages.error(request, 'Access denied.')
        return redirect('job_list')
    profile = get_object_or_404(EmployerProfile, user=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = profile
            job.save()
            messages.success(request, 'Job posted successfully.')
            return redirect('employer_jobs')
    else:
        form = JobForm()
    return render(request, 'jobs/create_job.html', {'form': form})

@login_required
def applicants_list(request, job_id):
    if not request.user.is_employer:
        messages.error(request, 'Access denied.')
        return redirect('job_list')
    profile = get_object_or_404(EmployerProfile, user=request.user)
    job = get_object_or_404(Job, id=job_id, employer=profile)
    applicants = Application.objects.filter(job=job).order_by('-applied_at')
    return render(request, 'jobs/applicants_list.html', {'job': job, 'applicants': applicants})

@login_required
def shortlist_applicant(request, app_id):
    if not request.user.is_employer:
        messages.error(request, 'Access denied.')
        return redirect('job_list')
    application = get_object_or_404(Application, id=app_id)
    profile = get_object_or_404(EmployerProfile, user=request.user)
    if application.job.employer != profile:
        messages.error(request, 'Access denied.')
        return redirect('job_list')
    application.status = 'SHORTLISTED'
    application.save()
    messages.success(request, 'Applicant shortlisted.')
    return redirect('applicants_list', job_id=application.job.id)

@login_required
def schedule_interview(request, app_id):
    if not request.user.is_employer:
        messages.error(request, 'Access denied.')
        return redirect('job_list')
    application = get_object_or_404(Application, id=app_id)
    profile = get_object_or_404(EmployerProfile, user=request.user)
    if application.job.employer != profile:
        messages.error(request, 'Access denied.')
        return redirect('job_list')
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.scheduled_by = profile
            interview.save()
            application.status = 'SHORTLISTED'
            application.save()
            messages.success(request, 'Interview scheduled.')
            return redirect('applicants_list', job_id=application.job.id)
    else:
        form = InterviewForm()
    return render(request, 'jobs/schedule_interview.html', {'form': form, 'application': application})
