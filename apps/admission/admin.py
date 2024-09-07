from django.contrib import admin
from .models import Course, Intake

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Intake)
class IntakeAdmin(admin.ModelAdmin):
    list_display = ['course', 'start_date', 'end_date']
    list_filter = ['course']
    search_fields = ['course__name']
