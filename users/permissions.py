from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return not request.method in SAFE_METHODS 

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated and request.user.is_staff):
            return False

        if request.method == 'POST':
            return False
        return True

    def has_object_permission(self, request, view, obj):
        return True