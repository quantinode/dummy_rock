from django.shortcuts import redirect
from .models import School

# URL prefixes that are always accessible (no subscription check)
_OPEN_PREFIXES = (
    '/',           # landing page (exact match handled below)
    '/login',
    '/register',
    '/logout',
    '/thank-you',
    '/admin',
    '/health',
    '/api/auth',
    '/static',
    '/media',
    '/favicon',
)

# Exact open paths
_OPEN_EXACT = {'/', '/thank-you/'}


def _is_open_path(path):
    if path in _OPEN_EXACT:
        return True
    for prefix in _OPEN_PREFIXES[1:]:  # skip '/' which is exact-matched above
        if path.startswith(prefix):
            return True
    return False


class SchoolBrandingMiddleware:
    """
    Injects request.school for authenticated users who belong to a school.
    base.html can then show school logo in the sidebar when request.school.logo exists.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.school = None
        if request.user.is_authenticated:
            if school_fk_id := getattr(request.user, 'school_id', None):
                try:
                    school = School.objects.get(pk=school_fk_id)
                    request.school = school
                    # Cache on user so model property can access it without extra query
                    request.user._cached_school = school
                except School.DoesNotExist:
                    pass
        return self.get_response(request)


class SubscriptionMiddleware:
    """
    Enforces subscription access control:
    - Expired users (beyond grace period) are redirected to /?subscription=expired
    - Warning/grace info is injected into request for the popup banner in base.html
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not _is_open_path(request.path):
            status = request.user.subscription_status

            if status == 'expired':
                # Force logout and redirect to landing pricing section
                from django.contrib.auth import logout
                logout(request)
                return redirect('/?subscription=expired')

            # Inject subscription info for the popup banner
            request.subscription_status = status
            request.subscription_days_remaining = request.user.subscription_days_remaining
        else:
            request.subscription_status = 'active'
            request.subscription_days_remaining = None

        return self.get_response(request)
