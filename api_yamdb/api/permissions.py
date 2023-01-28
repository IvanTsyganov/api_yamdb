from rest_framework import permissions

from reviews.models import User


class IsAuthenticatedOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
        )


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and
                    (
                            request.user.is_staff or request.user.role ==
                            User.ADMIN)
                    )


class GeneralPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and
                    (request.user.is_staff or
                     request.user.role == User.ADMIN) or
                    request.method in permissions.SAFE_METHODS)


class ReviewOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(request.method in permissions.SAFE_METHODS or
                    obj.author == request.user or
                    request.user.role == User.MODERATOR)
