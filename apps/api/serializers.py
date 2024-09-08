from rest_framework import serializers
from apps.admission.models import Course, Intake

class IntakeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Intake model.
    Handles the conversion of Intake model instances into JSON and vice versa.
    Includes fields: id, start_date, and end_date.
    """
    
    class Meta:
        model = Intake
        fields = ['id', 'start_date', 'end_date'] 

class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model.
    Handles both serialization and deserialization for Course instances, 
    and manages the nested relationship with Intakes.
    
    Fields:
    - id: Unique identifier for the Course.
    - name: Name of the Course.
    - intakes: Nested Intake objects, linked to the course.
    
    The 'intakes' field is defined with `many=True` to represent the one-to-many relationship 
    between Course and Intake. The field is read-only by default, meaning that Intake data 
    can only be read, not updated or created through this serializer.
    """
    intakes = IntakeSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'intakes'] #

    def create(self, validated_data):
        """
        Create and return a new Course instance, given the validated data.
        This method is automatically used by the Create API view.
        """
        return Course.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Course instance, given the validated data.
        This method is used by the Update API view.

        The instance refers to the Course object to be updated.
        The validated_data contains the updated values for the Course fields.
        """
        instance.name = validated_data.get('name', instance.name)  
        instance.save()
        return instance
