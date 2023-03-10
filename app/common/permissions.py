from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedOwnerPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return request.user.id == obj.owner.id
