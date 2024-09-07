from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Intake(models.Model):
    course = models.ForeignKey(Course, related_name='intakes', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.course.name}: {self.start_date} - {self.end_date}"
