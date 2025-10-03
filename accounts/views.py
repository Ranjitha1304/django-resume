from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import UserRegisterForm, JobSeekerProfileForm, EmployerProfileForm
from .models import JobSeekerProfile, EmployerProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import views as auth_views

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user = form.save(commit=False)
            # set flags
            if role == 'employer':
                user.is_employer = True
            else:
                user.is_jobseeker = True
            user.save()
            # create profile
            if user.is_jobseeker:
                JobSeekerProfile.objects.create(user=user, full_name=user.username)
            else:
                EmployerProfile.objects.create(user=user, company_name=user.username)
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    if user.is_employer:
        profile = get_object_or_404(EmployerProfile, user=user)
        return render(request, 'accounts/employer_dashboard.html', {'profile': profile})
    else:
        profile = get_object_or_404(JobSeekerProfile, user=user)
        return render(request, 'accounts/jobseeker_dashboard.html', {'profile': profile})

@login_required
def edit_profile(request):
    user = request.user
    if user.is_jobseeker:
        profile = get_object_or_404(JobSeekerProfile, user=user)
        if request.method == 'POST':
            form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated.')
                return redirect('dashboard')
        else:
            form = JobSeekerProfileForm(instance=profile)
        return render(request, 'accounts/edit_jobseeker.html', {'form': form})
    else:
        profile = get_object_or_404(EmployerProfile, user=user)
        if request.method == 'POST':
            form = EmployerProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated.')
                return redirect('dashboard')
        else:
            form = EmployerProfileForm(instance=profile)
        return render(request, 'accounts/edit_employer.html', {'form': form})
