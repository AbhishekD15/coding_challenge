from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User, Permission
from apps.admission.models import Course, Intake
from rest_framework_simplejwt.tokens import RefreshToken

class TestListCourses(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='Test Course')

    def test_list_courses(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_course'))
        response = self.client.get('/api/admission/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Check the length of the 'results' key

    def test_list_courses_with_intakes(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_course'))
        response = self.client.get('/api/admission/courses/?with_intakes=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Check the length of the 'results' key


class TestCreateCourse(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_course_no_permission(self):
        data = {'name': 'New Course'}
        response = self.client.post('/api/admission/courses/create/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_course_with_permission(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_course'))
        data = {'name': 'New Course'}
        response = self.client.post('/api/admission/courses/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_course_invalid_data(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_course'))
        data = {'name': ''}
        response = self.client.post('/api/admission/courses/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestRetrieveCourse(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.course = Course.objects.create(name='Test Course')
        self.client.force_authenticate(user=self.user)

    def test_retrieve_course_no_permission(self):
        response = self.client.get(f'/api/admission/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_course_with_permission(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_course'))
        response = self.client.get(f'/api/admission/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_non_existent_course(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_course'))
        response = self.client.get('/api/admission/courses/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestUpdateCourse(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.course = Course.objects.create(name='Test Course')
        self.client.force_authenticate(user=self.user)

    def test_update_course_no_permission(self):
        data = {'name': 'Updated Course'}
        response = self.client.put(f'/api/admission/courses/{self.course.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_course_with_permission(self):
        self.user.user_permissions.add(Permission.objects.get(codename='change_course'))
        data = {'name': 'Updated Course'}
        response = self.client.put(f'/api/admission/courses/{self.course.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_non_existent_course(self):
        self.user.user_permissions.add(Permission.objects.get(codename='change_course'))
        data = {'name': 'Updated Course'}
        response = self.client.put('/api/admission/courses/999/update/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestDeleteCourse(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.course = Course.objects.create(name='Test Course')
        self.client.force_authenticate(user=self.user)

    def test_delete_course_no_permission(self):
        response = self.client.delete(f'/api/admission/courses/{self.course.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_course_with_permission(self):
        self.user.user_permissions.add(Permission.objects.get(codename='delete_course'))
        response = self.client.delete(f'/api/admission/courses/{self.course.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_non_existent_course(self):
        self.user.user_permissions.add(Permission.objects.get(codename='delete_course'))
        response = self.client.delete('/api/admission/courses/999/delete/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestListIntakes(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.course = Course.objects.create(name='Test Course')
        self.client.force_authenticate(user=self.user)

    def test_list_intakes_no_permission(self):
        response = self.client.get(f'/api/admission/courses/{self.course.id}/intakes/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_intakes_with_permission(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_intake'))
        response = self.client.get(f'/api/admission/courses/{self.course.id}/intakes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)  # Assuming no intakes are created initially


class TestCreateIntake(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.course = Course.objects.create(name='Test Course')
        self.client.force_authenticate(user=self.user)

    def test_create_intake_no_permission(self):
        data = {'start_date': '2023-01-01', 'end_date': '2023-12-31'}
        response = self.client.post(f'/api/admission/courses/{self.course.id}/intakes/create/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_intake_with_permission(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_intake'))
        data = {'start_date': '2023-01-01', 'end_date': '2023-12-31'}
        response = self.client.post(f'/api/admission/courses/{self.course.id}/intakes/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_intake_invalid_data(self):
        self.user.user_permissions.add(Permission.objects.get(codename='add_intake'))
        data = {'start_date': '', 'end_date': ''}
        response = self.client.post(f'/api/admission/courses/{self.course.id}/intakes/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestRetrieveIntake(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.course = Course.objects.create(name='Test Course')
        self.client.force_authenticate(user=self.user)

    def test_retrieve_intake_no_permission(self):
        intake = Intake.objects.create(course=self.course, start_date='2023-01-01', end_date='2023-12-31')
        response = self.client.get(f'/api/admission/courses/{self.course.id}/intakes/{intake.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_intake_with_permission(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_intake'))
        intake = Intake.objects.create(course=self.course, start_date='2023-01-01', end_date='2023-12-31')
        response = self.client.get(f'/api/admission/courses/{self.course.id}/intakes/{intake.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_non_existent_intake(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_intake'))
        response = self.client.get(f'/api/admission/courses/{self.course.id}/intakes/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestUpdateIntake(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.course = Course.objects.create(name='Test Course')
        self.client.force_authenticate(user=self.user)

    def test_update_intake_no_permission(self):
        intake = Intake.objects.create(course=self.course, start_date='2023-01-01', end_date='2023-12-31')
        data = {'start_date': '2023-02-01', 'end_date': '2023-11-30'}
        response = self.client.put(f'/api/admission/courses/{self.course.id}/intakes/{intake.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_intake_with_permission(self):
        self.user.user_permissions.add(Permission.objects.get(codename='change_intake'))
        intake = Intake.objects.create(course=self.course, start_date='2023-01-01', end_date='2023-12-31')
        data = {'start_date': '2023-02-01', 'end_date': '2023-11-30'}
        response = self.client.put(f'/api/admission/courses/{self.course.id}/intakes/{intake.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_non_existent_intake(self):
        self.user.user_permissions.add(Permission.objects.get(codename='change_intake'))
        data = {'start_date': '2023-02-01', 'end_date': '2023-11-30'}
        response = self.client.put(f'/api/admission/courses/{self.course.id}/intakes/999/update/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestDeleteIntake(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.course = Course.objects.create(name='Test Course')
        self.client.force_authenticate(user=self.user)

    def test_delete_intake_no_permission(self):
        intake = Intake.objects.create(course=self.course, start_date='2023-01-01', end_date='2023-12-31')
        response = self.client.delete(f'/api/admission/courses/{self.course.id}/intakes/{intake.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_intake_with_permission(self):
        self.user.user_permissions.add(Permission.objects.get(codename='delete_intake'))
        intake = Intake.objects.create(course=self.course, start_date='2023-01-01', end_date='2023-12-31')
        response = self.client.delete(f'/api/admission/courses/{self.course.id}/intakes/{intake.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_non_existent_intake(self):
        self.user.user_permissions.add(Permission.objects.get(codename='delete_intake'))
        response = self.client.delete(f'/api/admission/courses/{self.course.id}/intakes/999/delete/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)