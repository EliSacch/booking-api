from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Count, Q
from django.contrib.auth.models import User

from .filters import AppointmentFilter
from .models import Appointment
from treatments.models import Treatment
from .serializers import StaffAppointmentSerializer, ClientAppointmentSerializer

from booking_api.permissions import IsOwner, IsStaffMember, IsStaffMemberOrOwner

from datetime import date as d


class AppointmentList(generics.ListCreateAPIView):
    """ List all appointments, or create a new one.
    The appointment list can be accessed by the staff members only,
     while each client can see only their own appointments """
    permission_classes = [ permissions.IsAuthenticated, IsStaffMember]
    queryset = Appointment.objects.order_by('-created_at')
    serializer_class = StaffAppointmentSerializer
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    search_fields = ['owner__username', 'client_name',]
    filterset_class = AppointmentFilter

    """ When the user creates an appointment, the reserved slots
     are automatically calculated """
    def perform_create(self, serializer):
        # If a user is selected, but the name is not entered, use username as client_name
        user = self.request.POST['owner']
        name = self.request.POST['client_name']
        if user != None and name == "":
            name = User.objects.get(id=user).username
        # Get the specific treatment duration and the start time
        treatment = self.request.POST['treatment']
        duration = Treatment.objects.get(title=treatment).duration
        start_time = int(self.request.POST['time'])
        # calculate end time
        end_time = start_time + duration

        serializer.save(end_time=end_time, client_name=name)


class MyAppointmentList(generics.ListCreateAPIView):
    """ List all appointments or create one for the logged in user.
    The appointment list can be accessed by the owners only """
    permission_classes = [ permissions.IsAuthenticated, IsOwner]
    queryset = Appointment.objects.order_by('-created_at')
    serializer_class = ClientAppointmentSerializer

    def filter_queryset(self, queryset):
        queryset = queryset.filter(owner=self.request.user)
        return super().filter_queryset(queryset)

    """ When the user creates an appointment, the reserved slots
     are automatically calculated """
    def perform_create(self, serializer):
        # Get the specific treatment duration
        treatment = self.request.POST['treatment']
        duration = Treatment.objects.get(title=treatment).duration
        start_time = int(self.request.POST['time'])
        end_time = start_time + duration

        """ When the user creates an appointment as client,
        the requesting user is set as owner """
        serializer.save(
            owner=self.request.user,
            client_name=self.request.user.username,
            end_time=end_time
            )


class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve or update an appointment if the owner.
    This view uses The appointment serializer, because
    clients cannot change the owner and/or client name """
    permission_classes = [ permissions.IsAuthenticated, IsOwner]
    queryset = Appointment.objects.order_by('-created_at')
    serializer_class = ClientAppointmentSerializer

    def perform_update(self, serializer):
        # Get the specific treatment duration
        treatment = self.request.POST['treatment']
        duration = Treatment.objects.get(title=treatment).duration
        start_time = int(self.request.POST['time'])
        end_time = start_time + duration
        
        serializer.save(end_time=end_time)


class ClientAppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve or update an appointment if a staff member.
    This views uses the ClientAppointmentSerializer because
    it is the one used by staff members, which can select the user
    and/or client name """
    permission_classes = [ permissions.IsAuthenticated, IsStaffMember]
    queryset = Appointment.objects.order_by('-created_at')
    serializer_class = StaffAppointmentSerializer

    def perform_update(self, serializer):
        # If a user is selected, but the name is not entered, use username as client_name
        user = self.request.POST['owner']
        name = self.request.POST['client_name']
        if user != None and name == "":
            name = User.objects.get(id=user).username
        # Get the specific treatment duration and the start time
        treatment = self.request.POST['treatment']
        duration = Treatment.objects.get(title=treatment).duration
        start_time = int(self.request.POST['time'])
        end_time = start_time + duration
        
        serializer.save(end_time=end_time, client_name=name)


