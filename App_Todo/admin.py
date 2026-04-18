from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'date', 'hours', 'created_at')  # 🔥 added
    list_filter = ('completed', 'date', 'created_at')  # 🔥 added date
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

