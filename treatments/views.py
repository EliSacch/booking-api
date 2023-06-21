from rest_framework import generics, permissions, status, filters

from .models import Treatment
from .serializers import TreatmentSerializer, ClientFacingTreatmentSerializer

from rest_framework.response import Response
from django.db.models import ProtectedError

from booking_api.permissions import IsStaffMemberOrReadOnly


class TreatmentList(generics.ListCreateAPIView):
    """ List all treatmentss, or create a new one if logged in as staff """
    permission_classes = [ permissions.IsAuthenticatedOrReadOnly, IsStaffMemberOrReadOnly ]
    queryset = Treatment.objects.order_by('-created_at')
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = ['title',]
    
    def get_serializer_class(self):
        if self.request.user.is_staff:
                return TreatmentSerializer
        return ClientFacingTreatmentSerializer


class TreatmentDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve the specific treatment and allow
    update and delete functionality """
    permission_classes = [ permissions.IsAuthenticatedOrReadOnly, IsStaffMemberOrReadOnly]
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer

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
