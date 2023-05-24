from rest_framework import generics, permissions

from .models import Appointment
from .serializers import AppointmentSerializer

from booking_api.permissions import IsOwner, IsStaffMember, IsStaffMemberOrOwner


class AllAppointmentList(generics.ListCreateAPIView):
    """ List all appointments, or create a new one.
    The appointment list can be accessed by the staff members only,
     while each client can see only their own appointments """
    permission_classes = [ permissions.IsAuthenticated, IsStaffMember]
    queryset = Appointment.objects.order_by('-created_at')
    serializer_class = AppointmentSerializer


class MyAppointmentList(generics.ListCreateAPIView):
    """ List all appointments or create one for the logged in user.
    The appointment list can be accessed by the owners only """
    permission_classes = [ permissions.IsAuthenticated, IsOwner]
    queryset = Appointment.objects.order_by('-created_at')
    serializer_class = AppointmentSerializer

    def filter_queryset(self, queryset):
        queryset = queryset.filter(owner=self.request.user)
        return super().filter_queryset(queryset)

    """ When the user creates an appointment as client,
    the requesting user is set as owner """
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve or update an appointment if the owner
    or a staff member """
    permission_classes = [ permissions.IsAuthenticated, IsStaffMemberOrOwner]
    queryset = Appointment.objects.order_by('-created_at')
    serializer_class = AppointmentSerializer
