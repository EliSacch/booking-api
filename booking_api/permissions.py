from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsOwnerOrReadOnly(permissions.BasePermission):
    """ This custom permission allows only the owner
    to access unsafe methods, but it gives read access to
    all other users """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsOwner(permissions.BasePermission):
    """ This permission allows only the owner to access
    all the methods. All other users are excluded """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsStaffMember(permissions.BasePermission):
    """ This permission allows access to the staff members only. 
    The owner has no access as well """
    def has_permission(self, request, view):
        return request.user.is_staff
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class IsStaffMemberOrOwner(permissions.BasePermission):
    """ This permission allows access to the staff members
    or to the owner """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff == True or obj.owner == request.user:
            return True
        else:
            return False
