from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    message = 'You are not authorized to perform any actions'
    '''
    Allow owners of an object to perform actions on it
    '''
    def has_permission(self, request, view):
        return request.user.is_active

    def has_object_permission(self, request, view):
        return obj.user == request.user
