from rest_framework import generics, permissions
from django.db.models import Q

from .models import Appointment
from services.models import Service
from .serializers import StaffAppointmentSerializer, ClientAppointmentSerializer

from booking_api.permissions import IsOwner, IsStaffMember, IsStaffMemberOrOwner


class AllAppointmentList(generics.ListCreateAPIView):
    """ List all appointments, or create a new one.
    The appointment list can be accessed by the staff members only,
     while each client can see only their own appointments """
    permission_classes = [ permissions.IsAuthenticated, IsStaffMember]
    queryset = Appointment.objects.order_by('-created_at')
    serializer_class = StaffAppointmentSerializer

    """ When the user creates an appointment, the reserved slots
     are automatically calculated """
    def perform_create(self, serializer):
        # Get the specific service duration
        service = self.request.POST['service']
        duration = Service.objects.filter(title=service).first().duration
        start_time = int(self.request.POST['time'])
        end_time = start_time + duration
        serializer.save(end_time=end_time)


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
        # Get the specific service duration
        service = self.request.POST['service']
        duration = Service.objects.filter(title=service).first().duration
        start_time = int(self.request.POST['time'])
        end_time = start_time + duration

        """ When the user creates an appointment as client,
        the requesting user is set as owner """
        serializer.save(owner=self.request.user, client_name=self.request.user.username, end_time=end_time)


class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve or update an appointment if the owner.
    This view uses The appointment serializer, because
    clients cannot change the owner and/or client name """
    permission_classes = [ permissions.IsAuthenticated, IsOwner]
    queryset = Appointment.objects.order_by('-created_at')
    serializer_class = ClientAppointmentSerializer

    def perform_update(self, serializer):
        # Get the specific service duration
        service = self.request.POST['service']
        duration = Service.objects.filter(title=service).first().duration
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
        # Get the specific service duration
        service = self.request.POST['service']
        duration = Service.objects.filter(title=service).first().duration
        start_time = int(self.request.POST['time'])
        end_time = start_time + duration
        
        serializer.save(end_time=end_time)
