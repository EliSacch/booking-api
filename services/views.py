from rest_framework import generics, permissions

from .models import Service
from .serializers import ServiceSerializer, ClientFacingServiceSerializer

from booking_api.permissions import IsStaffMember


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
    queryset = Service.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ClientFacingServiceSerializer


class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve the specific service and allow
    update and delete functionality """
    permission_classes = [ permissions.IsAuthenticated, IsStaffMember]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
