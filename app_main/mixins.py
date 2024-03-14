from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden

class IsSuperuserMixin(UserPassesTestMixin):
    """ Mixin to validate superuser """
    
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to access this page.")
