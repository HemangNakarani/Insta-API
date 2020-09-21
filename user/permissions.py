from rest_framework import permissions


class ViewAccessPermission(permissions.BasePermission):
    message = 'If you are not following then you are not allowed to see their Profile'

    def has_object_permission(self, request, view, opposite_user):
        print(opposite_user, request.user)
        self_user = request.user
        if opposite_user != self_user:
            if opposite_user in self_user.following.all():
                return True
            else:
                return False
        else:
            return True
