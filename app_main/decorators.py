from functools import wraps
from django.http import Http404


def is_superuser(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404("Not found")

        return func(request, *args, **kwargs)
    return wrapper
