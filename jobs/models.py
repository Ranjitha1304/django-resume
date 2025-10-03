from django.db import models
from django.utils.text import slugify
from accounts.models import EmployerProfile, JobSeekerProfile

JOB_TYPE_CHOICES = (('FT', 'Full-time'), ('PT', 'Part-time'), ('IN', 'Internship'), ('CT', 'Contract'))
APPLICATION_STATUS = (('APPLIED', 'Applied'), ('SHORTLISTED', 'Shortlisted'), ('REJECTED', 'Rejected'), ('HIRED', 'Hired'))

class Job(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, blank=True)
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    salary_min = models.PositiveIntegerField(null=True, blank=True)
    salary_max = models.PositiveIntegerField(null=True, blank=True)
    job_type = models.CharField(max_length=2, choices=JOB_TYPE_CHOICES, default='FT')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_base = slugify(self.title)[:200]
            # ensure uniqueness if required by adding id later after save (simple here)
            self.slug = slug_base
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    jobseeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='applications/%Y/%m/%d/', blank=True, null=True)
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='APPLIED')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'jobseeker')

    def __str__(self):
        return f"{self.job.title} - {self.jobseeker.full_name or self.jobseeker.user.username}"

class Interview(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    scheduled_by = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveSmallIntegerField(default=30)
    mode = models.CharField(max_length=50, default='Online')  # or On-site
    meeting_link = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=30, default='SCHEDULED')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Interview for {self.application} at {self.scheduled_at}"
