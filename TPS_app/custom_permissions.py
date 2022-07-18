from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
   def has_permission(self, request, view):
      return request.user.is_staff

class IsCapitan(BasePermission):
   def has_permission(self, request, view):
      return request.user.is_capitan