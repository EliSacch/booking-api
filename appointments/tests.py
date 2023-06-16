from django.contrib.auth.models import User
from .models import Appointment
#from treatments.models import Service

from rest_framework import status
from rest_framework.test import APITestCase


class AppointmentListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='Admin', password='admin', is_staff=True)
        User.objects.create_user(username='Client', password='client')
        #Service.objects.create(title='Color', duration=100)

    def test_is_staff(self):
        admin = User.objects.get(username='Admin')
        self.assertEqual(admin.is_staff, True)

    def test_not_loggedin_user_cannot_list_appointments(self):
        response = self.client.get('/my-appointments/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_loggedin_client_can_list_their_appointments(self):
        self.client.login(username='Client', password='client')
        response = self.client.get('/my-appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_appointment(self):
        self.client.login(username='Client', password='client')
        client = User.objects.get(username='Client')
        #service = Service.objects.get(title='Color')
        #response = self.client.post('/my-appointments/', {'owner': client, 'service': service, 'date': '2023-08-09', 'time': 900})
        count = Appointment.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_cannot_list_all_appointments(self):
        self.client.login(username='Client', password='client')
        response = self.client.get('/appointments/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_list_all_appointments(self):
        self.client.login(username='Admin', password='admin')
        response = self.client.get('/appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AppointmentDetailViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='Admin', password='admin', is_staff=True)
        User.objects.create_user(username='Client', password='client')
       # Service.objects.create(title='Color', duration=100)
        admin = User.objects.get(username='Admin')
        client = User.objects.get(username='Client')
        #service = Service.objects.get(title='Color')
        #Appointment.objects.create(owner=admin, service=service, date='2023-08-09', time=1300, end_time=1400)
        #Appointment.objects.create(owner=client, service=service, date='2023-08-10', time=1100, end_time=1200)

    def test_staff_can_retrieve_any_appointment_using_valid_id(self):
        self.client.login(username='Admin', password='admin')
        response = self.client.get('/appointments/2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_appointment_using_invalid_id(self):
        self.client.login(username='Admin', password='admin')
        response = self.client.get('/appointments/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_client_can_retrieve_their_appointment_using_valid_id(self):
        self.client.login(username='Client', password='client')
        response = self.client.get('/my-appointments/2/')
        self.assertEqual(response.data['date'], '2023-08-10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_cannot_retrieve_appointment_they_dont_own(self):
        self.client.login(username='Client', password='client')
        response = self.client.get('/my-appointments/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_client_can_update_own_appointment(self):
        self.client.login(username='Client', password='client')
        client = User.objects.get(username='Client')
        service = Service.objects.get(title='Color')
        response = self.client.put('/my-appointments/2/', {'owner': client, 'service': service, 'date': '2023-08-10', 'time': 900})
        appointment = Appointment.objects.filter(pk=2).first()
        self.assertEqual(appointment.time, 900)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_cant_update_another_users_appointment(self):
        self.client.login(username='Client', password='client')
        response = self.client.put('/my-appointments/1/', {'time': 900})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_staff_can_update_another_users_appointment(self):
        self.client.login(username='Admin', password='admin')
        client = User.objects.get(username='Client')
        #service = Service.objects.get(title='Color')
        #response = self.client.put('/appointments/2/', {'owner': client, 'service': service, 'date': '2023-08-10', 'time': 1000})
        #self.assertEqual(response.status_code, status.HTTP_200_OK)
