from django.contrib import admin

from .models import Task, TaskAttachment

admin.site.register(Task)
admin.site.register(TaskAttachment)
