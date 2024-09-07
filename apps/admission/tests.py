from django.test import TestCase
from .models import Course, Intake
from datetime import date

class CourseModelTest(TestCase):
    """
    Test case for the Course model.
    """
    
    def setUp(self):
        """
        Set up a test course instance.
        This method is run before every test case.
        """
        self.course = Course.objects.create(name="Test Course")

    def test_course_creation(self):
        """
        Ensure that a Course instance is created correctly.
        """
        # Assert the course name is correctly saved
        self.assertEqual(self.course.name, "Test Course")
    
    def test_course_str(self):
        """
        Test the string representation of a Course instance.
        """
        # Assert the string representation returns the course name
        self.assertEqual(str(self.course), "Test Course")


class IntakeModelTest(TestCase):
    """
    Test case for the Intake model.
    """
    
    def setUp(self):
        """
        Set up a test course and intake instance.
        This method is run before every test case.
        """
        self.course = Course.objects.create(name="Test Course")
        self.intake = Intake.objects.create(
            course=self.course, 
            start_date=date.today(), 
            end_date=date.today()
        )
    
    def test_intake_creation(self):
        """
        Ensure that an Intake instance is created and linked to a Course.
        """
        # Assert the intake is correctly associated with the course
        self.assertEqual(self.intake.course.name, "Test Course")
    
    def test_intake_str(self):
        """
        Test the string representation of an Intake instance.
        """
        # Assert the string representation includes the course name and dates
        expected_str = f"Test Course: {self.intake.start_date} - {self.intake.end_date}"
        self.assertEqual(str(self.intake), expected_str)

