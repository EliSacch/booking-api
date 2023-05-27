from rest_framework import generics, permissions

from .models import Appointment
from .serializers import AppointmentSerializer, ClientAppointmentSerializer

from booking_api.permissions import IsOwner, IsStaffMember, IsStaffMemberOrOwner


class AllAppointmentList(generics.ListCreateAPIView):
    """ List all appointments, or create a new one.
    The appointment list can be accessed by the staff members only,
     while each client can see only their own appointments """
    permission_classes = [ permissions.IsAuthenticated, IsStaffMember]
    queryset = Appointment.objects.order_by('-created_at')
    serializer_class = ClientAppointmentSerializer

    """ When the user creates an appointment, the reserved slots
     are automatically calculated 
    def perform_create(self, serializer):
        # For the moment we set 1h30 duration for each appointment,
        # but then we will change it based on the service
        duration = 150
        duration_range = int(duration / 50)
        start_time = self.request.time
        slots = []

        for slot in range(0,duration_range):
            slots += [start_time + (slot*50)]

        serializer.save(slots=slots)
        """


class MyAppointmentList(generics.ListCreateAPIView):
    """ List all appointments or create one for the logged in user.
    The appointment list can be accessed by the owners only """
    permission_classes = [ permissions.IsAuthenticated, IsOwner]
    queryset = Appointment.objects.order_by('-created_at')
    serializer_class = AppointmentSerializer

    def filter_queryset(self, queryset):
        queryset = queryset.filter(owner=self.request.user)
        return super().filter_queryset(queryset)

    """ When the user creates an appointment, the reserved slots
     are automatically calculated """
    def perform_create(self, serializer):
        # For the moment we set 1h30 duration for each appointment,
        # but then we will change it based on the service
        """duration = 150
        duration_range = int(duration / 50)
        start_time = self.request.time
        slots = []

        for slot in range(0,duration_range):
            slots += [start_time + (slot*50)]"""

        """ When the user creates an appointment as client,
        the requesting user is set as owner """
        serializer.save(owner=self.request.user)


class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve or update an appointment if the owner.
    This view uses The appointment serializer, because
    clients cannot change the owner and/or client name """
    permission_classes = [ permissions.IsAuthenticated, IsOwner]
    queryset = Appointment.objects.order_by('-created_at')
    serializer_class = AppointmentSerializer


class ClientAppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve or update an appointment if a staff member.
    This views uses the ClientAppointmentSerializer because
    it is the one used by staff members, which can select the user
    and/or client name """
    permission_classes = [ permissions.IsAuthenticated, IsStaffMember]
    queryset = Appointment.objects.order_by('-created_at')
    serializer_class = ClientAppointmentSerializer
