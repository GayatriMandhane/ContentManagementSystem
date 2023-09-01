from rest_framework import permissions
from . import views


# class IsAuthorOrAdmin(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         # Admin can perform any action
#         if request.user.is_superuser:
#             return True

#         # Author can perform actions on their own content
#         return obj.author == request.user
    
# class HasValidToken(permissions.BasePermission):
#     def has_permission(self):
#         try:
#             if views.userLogin.access_token:
#                 print(views.userLogin.access_token)
#                 return True
#         except Exception as e:
#             return False