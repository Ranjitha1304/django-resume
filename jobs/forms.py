from django import forms
from .models import Job, Application, Interview

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'requirements', 'location', 'salary_min', 'salary_max', 'job_type', 'is_active', 'expiry_date']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            if not resume.name.lower().endswith('.pdf'):
                raise forms.ValidationError('Only PDF files are allowed for resumes.')
            content_type = getattr(resume, 'content_type', None)
            if content_type and content_type != 'application/pdf':
                raise forms.ValidationError('Uploaded file is not a valid PDF.')
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Resume file size must be under 5MB.')
        return resume

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['scheduled_at', 'duration_minutes', 'mode', 'meeting_link', 'notes']
        widgets = {'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local'})}
