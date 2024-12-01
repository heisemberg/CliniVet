from rest_framework import permissions

class IsOwnerOrDoctorOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners, doctors, or admins to view an appointment.
    """
    def has_object_permission(self, request, view, obj):
        # Admins can do anything
        if request.user.is_staff:
            return True
        # Only the owner or the doctor can view the appointment
        return obj.client == request.user.client or obj.availability.doctor == request.user.doctor

    
class IsDoctorOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow doctors or admins to edit or delete a medical record.
    """
    def has_object_permission(self, request, view, obj):
        # Admins can do anything
        if request.user.is_staff:
            return True
        # Only the doctor can edit or delete
        return obj.doctor == request.user.doctor
    
    
class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Admins can do anything
        if request.user.is_staff:
            return True
        # Only the owner can edit or delete
        return obj.owner == request.user.client
    
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit or delete, but allow read-only access to others.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class IsDoctorOrSellerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow doctors, sellers, or admins to create sales.
    """
    def has_permission(self, request, view):
        # Allow read-only access to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow create access to doctors, sellers, and admins
        return request.user.is_staff or hasattr(request.user, 'doctor') or hasattr(request.user, 'seller')