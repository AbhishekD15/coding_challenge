import csv
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from django.contrib import admin
from django.http import HttpResponse
from .models import Course, Intake

# Export selected courses to CSV
def export_courses_to_csv(modeladmin, request, queryset):
    """
    Custom admin action to export course data to CSV.
    Exports each selected course and its associated intakes.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="courses.csv"'

    writer = csv.writer(response)
    writer.writerow(['Course Name', 'Intake Start Date', 'Intake End Date'])

    for course in queryset:
        for intake in course.intakes.all():
            writer.writerow([course.name, intake.start_date, intake.end_date])

    return response

export_courses_to_csv.short_description = "Export selected courses to CSV"

# Change widget for date fields in Intake
class IntakeAdminForm(ModelForm):
    class Meta:
        model = Intake
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # Check if end date is before start date
        if end_date and start_date and end_date < start_date:
            raise ValidationError({
                'end_date': "End date cannot be earlier than the start date."
            })
        return cleaned_data

# Inline admin for managing intakes directly in the course admin page
class IntakeInline(admin.TabularInline):
    """
    Inline admin for Intake objects within the Course admin page.
    """
    model = Intake
    extra = 1  # Allows adding one new intake directly from the course page, could be updated to allow multiple

# Register the Course model with custom actions and inline intake editor
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Custom admin interface for Course with CSV export, inline intake editor, and bulk actions.
    """
    list_display = ['name']
    search_fields = ['name']
    actions = [export_courses_to_csv]  # Register custom CSV export action
    inlines = [IntakeInline]  # Allows editing intakes directly in the course admin page

# Register the Intake model with custom form and date pickers
@admin.register(Intake)
class IntakeAdmin(admin.ModelAdmin):
    list_display = ['course', 'start_date', 'end_date']
    list_filter = ['course', 'start_date', 'end_date']
    search_fields = ['course__name', 'start_date', 'end_date']
    autocomplete_fields = ['course']  # Enable autocomplete on the course field

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course":
            kwargs["queryset"] = Course.objects.all().order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
