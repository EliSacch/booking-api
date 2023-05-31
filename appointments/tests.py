from django.contrib.auth.models import User
from .models import Appointment
from profiles.models import Profile
from services.models import Service
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='Test', password='test')
        User.objects.create_user(username='Admin', password='admin', is_staff=True)
        Service.objects.create(title='Color', duration=100)
        admin = User.objects.get(username='Admin')
        service = Service.objects.get(title='Color')
        Appointment.objects.create(owner=admin, service=service, date='2023-08-09', time=1300)

    def test_is_staff(self):
        admin = User.objects.get(username='Admin')
        self.assertEqual(admin.is_staff, True)

    def test_not_loggedin_user_cannot_list_appointments(self):
        response = self.client.get('/my-appointments/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print(response.data)
        print(len(response.data))

    def test_loggedin_client_can_list_appointments(self):
        self.client.login(username='Test', password='test')
        response = self.client.get('/my-appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_appointment(self):
        self.client.login(username='Test', password='test')
        client = User.objects.get(username='Test')
        service = Service.objects.get(title='Color')
        response = self.client.post('/my-appointments/', {'owner': client, 'service': service, 'date': '2023-08-09', 'time': 900})
        count = Appointment.objects.count()
        self.assertEqual(count, 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_cannot_list_all_appointments(self):
        self.client.login(username='Test', password='test')
        response = self.client.get('/appointments/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print(response.data)
        print(len(response.data))

    def test_staff_can_list_all_appointments(self):
        self.client.login(username='Admin', password='admin')
        response = self.client.get('/appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))
