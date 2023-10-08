from rest_framework.permissions import BasePermission


class EducationItemAccess(BasePermission):
    def has_permission(self, request, view):
        print(request.method)
        if request.method == 'GET':
            return request.user.is_authenticated
        elif request.method == 'POST':
            return request.user.is_authenticated and not self.user_is_moderator(request)
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        print(request.method)
        if not request.user.is_authenticated:
            return False

        if request.method in ['GET', 'PUT', 'PATCH']:
            return obj.owner == request.user or self.user_is_moderator(request)
        elif request.method == 'DELETE':
            return obj.owner == request.user
        else:
            return False

    @staticmethod
    def user_is_moderator(request):
        return request.user.groups.filter(name='moderator_group').exists()