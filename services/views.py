from rest_framework import generics, permissions

from .models import Service
from .serializers import ServiceSerializer

from booking_api.permissions import IsOwner, IsStaffMember, IsStaffMemberOrOwner


class ServiceList(generics.ListCreateAPIView):
    """ List all services, or create a new one.
    This services list can be accessed by the staff members only """
    permission_classes = [ permissions.IsAuthenticated, IsStaffMember]
    queryset = Service.objects.order_by('-created_at')
    serializer_class = ServiceSerializer


class ClientFacingServiceList(generics.ListAPIView):
    """ List all services, accessible to clients.
    Clients can only review the available services, but they cannot edit them """
    permission_classes = [ permissions.IsAuthenticated ]
    queryset = Service.objects.order_by('-created_at')
    serializer_class = ServiceSerializer


class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve the specific service and allow
    update and delete functionality """
    permission_classes = [ permissions.IsAuthenticated, IsStaffMember]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer