from rest_framework import generics, permissions

from .models import Appointment
from services.models import Service
from .serializers import AppointmentSerializer, ClientAppointmentSerializer

from booking_api.permissions import IsOwner, IsStaffMember, IsStaffMemberOrOwner


""" This function is used in all views to calculate the slots
reserved for a specific appointment, from the selected time """
def calculate_slots(start, duration):
    duration_range = int(duration / 50)
    start_time = start
    slots = []

    for slot in range(0,duration_range):
        slots += [start_time + (slot*50)]
    return slots


class AllAppointmentList(generics.ListCreateAPIView):
    """ List all appointments, or create a new one.
    The appointment list can be accessed by the staff members only,
     while each client can see only their own appointments """
    permission_classes = [ permissions.IsAuthenticated, IsStaffMember]
    queryset = Appointment.objects.order_by('-created_at')
    serializer_class = ClientAppointmentSerializer

    """ When the user creates an appointment, the reserved slots
     are automatically calculated """
    def perform_create(self, serializer):
        # Get the specific service duration
        service_id = int(self.request.POST['service'])
        duration = Service.objects.filter(id=service_id).first().duration
        start_time = int(self.request.POST['time'])
        slots = calculate_slots(start_time, duration)
        serializer.save(slots=slots)


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
        # Get the specific service duration
        service_id = int(self.request.POST['service'])
        duration = Service.objects.filter(id=service_id).first().duration
        start_time = int(self.request.POST['time'])
        slots = calculate_slots(start_time, duration)

        """ When the user creates an appointment as client,
        the requesting user is set as owner """
        serializer.save(owner=self.request.user, client_name=self.request.user.username, slots=slots)


class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve or update an appointment if the owner.
    This view uses The appointment serializer, because
    clients cannot change the owner and/or client name """
    permission_classes = [ permissions.IsAuthenticated, IsOwner]
    queryset = Appointment.objects.order_by('-created_at')
    serializer_class = AppointmentSerializer

    def perform_update(self, serializer):
        # Get the specific service duration
        service_id = int(self.request.POST['service'])
        duration = Service.objects.filter(id=service_id).first().duration
        start_time = int(self.request.POST['time'])
        slots = calculate_slots(start_time, duration)
        
        serializer.save(slots=slots)


class ClientAppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve or update an appointment if a staff member.
    This views uses the ClientAppointmentSerializer because
    it is the one used by staff members, which can select the user
    and/or client name """
    permission_classes = [ permissions.IsAuthenticated, IsStaffMember]
    queryset = Appointment.objects.order_by('-created_at')
    serializer_class = ClientAppointmentSerializer

    def perform_update(self, serializer):
        # Get the specific service duration
        service_id = int(self.request.POST['service'])
        duration = Service.objects.filter(id=service_id).first().duration
        start_time = int(self.request.POST['time'])
        slots = calculate_slots(start_time, duration)
        
        serializer.save(slots=slots)
