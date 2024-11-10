from functools import wraps
from rest_framework.response import Response
from rest_framework import status

PERMISSIONS = {
    'admin': ['admin_permission'], # add more permission on the list
    'standard': ['standard_permission']
}

def get_user_permissions(user):
    all_permissions = set()
    for group in user.groups.all():
        all_permissions.update(PERMISSIONS.get(group.name, []))
    return all_permissions

# custom permission check
def check_permission(required_permissions):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_permissions = get_user_permissions(request.user)
            if not any(permission in user_permissions for permission in required_permissions):
                return Response({'message': 'Permission denied!'}, status=status.HTTP_403_FORBIDDEN)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


class XAccessTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get('x-access-token')
        if token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        response = self.get_response(request)
        return response


