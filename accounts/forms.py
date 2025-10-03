from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, JobSeekerProfile, EmployerProfile

class UserRegisterForm(UserCreationForm):
    ROLE_CHOICES = (('jobseeker', 'Job Seeker'), ('employer', 'Employer'))
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['full_name', 'phone', 'location', 'about', 'experience_years', 'skills', 'resume']

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            # Check extension
            if not resume.name.lower().endswith('.pdf'):
                raise forms.ValidationError('Only PDF files are allowed for resumes.')
            # Check content type if present
            content_type = getattr(resume, 'content_type', None)
            if content_type and content_type != 'application/pdf':
                raise forms.ValidationError('Uploaded file is not a valid PDF.')
            # Size limit 5MB
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Resume file size must be under 5MB.')
        return resume

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'website', 'logo', 'description', 'phone', 'address']
