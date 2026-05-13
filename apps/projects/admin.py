from django.contrib import admin

from .models import Project, ProjectAttachment, ProjectMember

admin.site.register(Project)
admin.site.register(ProjectMember)
admin.site.register(ProjectAttachment)
