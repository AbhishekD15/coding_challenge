from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User, Permission
from apps.admission.models import Course, Intake

class TestListCourses(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='Test Course')

    def test_list_courses(self):
        response = self.client.get('/api/admission/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Course')

    def test_list_courses_with_intakes(self):
        intake = Intake.objects.create(course=self.course, start_date='2023-01-01', end_date='2023-12-31')
        response = self.client.get('/api/admission/courses/?with_intakes=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Course')
        self.assertEqual(len(response.data[0]['intakes']), 1)
        self.assertEqual(response.data[0]['intakes'][0]['start_date'], '2023-01-01')
        self.assertEqual(response.data[0]['intakes'][0]['end_date'], '2023-12-31')


class TestCreateCourse(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.user_permissions.add(Permission.objects.get(codename='add_course'))
        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        data = {'name': 'New Course'}
        response = self.client.post('/api/admission/courses/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Course')

    def test_create_course_no_permission(self):
        self.user.user_permissions.remove(Permission.objects.get(codename='add_course'))
        data = {'name': 'New Course'}
        response = self.client.post('/api/admission/courses/create/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestRetrieveCourse(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.user_permissions.add(Permission.objects.get(codename='view_course'))
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='Test Course')

    def test_retrieve_course(self):
        response = self.client.get(f'/api/admission/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Course')

    def test_retrieve_course_no_permission(self):
        self.user.user_permissions.remove(Permission.objects.get(codename='view_course'))
        response = self.client.get(f'/api/admission/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestUpdateCourse(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.user_permissions.add(Permission.objects.get(codename='change_course'))
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='Test Course')

    def test_update_course(self):
        data = {'name': 'Updated Course'}
        response = self.client.put(f'/api/admission/courses/{self.course.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Course')

    def test_update_course_no_permission(self):
        self.user.user_permissions.remove(Permission.objects.get(codename='change_course'))
        data = {'name': 'Updated Course'}
        response = self.client.put(f'/api/admission/courses/{self.course.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestDeleteCourse(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.user_permissions.add(Permission.objects.get(codename='delete_course'))
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='Test Course')

    def test_delete_course(self):
        response = self.client.delete(f'/api/admission/courses/{self.course.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())

    def test_delete_course_no_permission(self):
        self.user.user_permissions.remove(Permission.objects.get(codename='delete_course'))
        response = self.client.delete(f'/api/admission/courses/{self.course.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)