from django.core.exceptions import PermissionDenied


class PermissionHandlerMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        owner = self.request.user.id == self.object.user_id
        if not owner and not request.user.is_superuser:
            raise PermissionDenied
        return response