from rest_framework.permissions import BasePermission

class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Instance must have an attribute named `author`.
        return obj.author == request.user
