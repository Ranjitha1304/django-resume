from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, EmployerProfile, JobSeekerProfile

admin.site.register(User, UserAdmin)
admin.site.register(EmployerProfile)
admin.site.register(JobSeekerProfile)
