from rest_framework import serializers
from apps.admission.models import Course, Intake

class IntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intake
        fields = ['id', 'start_date', 'end_date']

class CourseSerializer(serializers.ModelSerializer):
    intakes = IntakeSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'intakes']
