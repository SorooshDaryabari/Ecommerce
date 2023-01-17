from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrCommentCreatorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.user.is_staff:
            return True
        return request.user == obj.user
