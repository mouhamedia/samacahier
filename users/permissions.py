from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Permission pour vérifier si l'utilisateur est le propriétaire."""
    
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class IsBoutiquier(permissions.BasePermission):
    """Permission pour les boutiquiers."""
    
    def has_permission(self, request, view):
        return request.user and request.user.role == 'boutiquier'


class IsClient(permissions.BasePermission):
    """Permission pour les clients."""
    
    def has_permission(self, request, view):
        return request.user and request.user.role == 'client'
