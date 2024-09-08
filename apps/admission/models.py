from django.db import models
from django.core.exceptions import ValidationError

class Course(models.Model):
    name = models.CharField(max_length=255, db_index=True)  # Index for faster name lookups

    def __str__(self):
        return self.name

class Intake(models.Model):
    course = models.ForeignKey(Course, related_name='intakes', on_delete=models.CASCADE, db_index=True)  # Indexed FK
    start_date = models.DateField(db_index=True)  # Indexed for faster date queries
    end_date = models.DateField(db_index=True)

    def __str__(self):
        return f"{self.course.name}: {self.start_date} - {self.end_date}"

    def clean(self):
        # Model-level validation for start and end date
        if self.end_date < self.start_date:
            raise ValidationError('End date cannot be earlier than start date.')
