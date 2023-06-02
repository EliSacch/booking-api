from django.db.models import Count, Q
from rest_framework import generics, permissions, filters

from .models import Profile
from .serializers import ProfileSerializer, ClientSerializer

from booking_api.permissions import IsOwner, IsStaffMember

from datetime import date


class ProfileList(generics.ListAPIView):
    """ List all profiles.
    No create view as profile creation is handled by django signals.
    The profiles list can be acceed by the staff members only,
    This is why it uses the ClientSerializer """
    permission_classes = [permissions.IsAuthenticated, IsStaffMember]
    queryset = Profile.objects.annotate(
        appointments_count=Count('owner__appointment', distinct=True),
        has_appointments_today = Count('owner__appointment', filter=Q(owner__appointment__date=date.today()), distinct=True),
    ).order_by('-created_at')
    serializer_class = ClientSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ['owner__username']
    ordering_fields = [
        'appointments_count',
        'has_appointments_today'
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """ Retrieve or update a profile if you're the owner.
    This is the client facing profile detail view 
    this is why it uses the Profile Serializer """
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Profile.objects.order_by('-created_at')
    serializer_class = ProfileSerializer


class ClientProfileDetail(generics.RetrieveUpdateAPIView):
    """ Retrieve or update a client profile profile
    if you're a staff member.
    This is the staff facing profile detail view 
    this is why it uses the Client Serializer """
    permission_classes = [permissions.IsAuthenticated, IsStaffMember]
    queryset = Profile.objects.order_by('-created_at')
    serializer_class = ClientSerializer
