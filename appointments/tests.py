from django.contrib.auth.models import User
from .models import Appointment
from services.models import Service
from rest_framework import status
from rest_framework.test import APITestCase


class AppointmentListViewTests(APITestCase):
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

    def test_loggedin_client_can_list_their_appointments(self):
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


"""class AppointmentDetailViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='Test', password='test')
        User.objects.create_user(username='Admin', password='admin', is_staff=True)
        Service.objects.create(title='Color', duration=100)
        admin = User.objects.get(username='Admin')
        client = User.objects.get(username='Test')
        service = Service.objects.get(title='Color')
        Appointment.objects.create(owner=admin, service=service, date='2023-08-11', time=1300)
        Appointment.objects.create(owner=client, service=service, date='2023-08-10', time=1000)

    def test_staff_can_retrieve_any_appointment_using_valid_id(self):
        self.client.login(username='Admin', password='admin')
        response = self.client.get('/appointments/11/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_appointment_using_invalid_id(self):
        self.client.login(username='Admin', password='admin')
        response = self.client.get('/appointments/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)"""

"""def test_client_can_retrieve_their_appointment_using_valid_id(self):
        self.client.login(username='Test', password='test')
        response = self.client.get('/my-appointments/1/')
        self.assertEqual(response.data['date'], '2023-08-09')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_cannot_retrieve_appointment_they_dont_own(self):
        self.client.login(username='Test', password='test')
        response = self.client.get('/my-appointments/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_client_can_update_own_appointment(self):
        self.client.login(username='Test', password='test')
        response = self.client.put('/my-appointments/2/', {'time': 900})
        appointment = Appointment.objects.filter(pk=2).first()
        self.assertEqual(appointment.time, 900)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_cant_update_another_users_appointment(self):
        self.client.login(username='Test', password='test')
        response = self.client.put('/my-appointments/1/', {'time': 900})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_staff_can_update_another_users_appointment(self):
        self.client.login(username='Admin', password='admin')
        response = self.client.put('/appointments/2/', {'time': 1100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)"""
