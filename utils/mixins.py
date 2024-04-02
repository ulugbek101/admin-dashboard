from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden


class IsSuperuserOrAdminMixin(UserPassesTestMixin):
    """ Mixin to validate superuser or admin """

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_admin

    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to access this page.")
