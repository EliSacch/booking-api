from rest_framework import permissions


""" This custom permission allows only the owner
to access unsafe methods, but it gives read access to
all other users """
class IsOwnerOrReadOnly(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    return obj.owner == request.user


""" This permission allows only the owner to access
all the methods. All other users are excluded """
class IsOwner(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    return obj.owner == request.user


""" This permission allows access to the staff members only. 
The owner has no access as well """
class IsStaffMember(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    return request.user.isStaff