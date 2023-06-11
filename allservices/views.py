from rest_framework import generics, permissions, status

from .models import Service
from .serializers import ServiceSerializer, ClientFacingServiceSerializer

from rest_framework.response import Response
from django.db.models import ProtectedError

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
    permission_classes = [ permissions.SAFE_METHODS ]
    queryset = Service.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ClientFacingServiceSerializer


class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve the specific service and allow
    update and delete functionality """
    permission_classes = [ permissions.IsAuthenticated, IsStaffMember]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    # The following code to catch ProtectedError is from Stacjoverflow - Link in README
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        # if protected, cannot be deleted, show error message
        except ProtectedError as exception:
            message = f"You cannot delete this Service because it is being used. Please, set it to inactive."
            response_msg = {
                "error": {"message": message},
            }
            return Response(response_msg, status=status.HTTP_400_BAD_REQUEST)
    # End of code from Stackoverflow
