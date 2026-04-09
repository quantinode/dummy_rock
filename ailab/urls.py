from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns = [
    path('health/', lambda r: JsonResponse({'status': 'ok'})),
    path('admin/', admin.site.urls),
    path('login/', user_views.login_page, name='login'),
    path('register/', user_views.register_page, name='register'),
    path('logout/', user_views.logout_page, name='logout'),
    # Password reset flow
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html', email_template_name='users/password_reset_email.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('', include('landing.urls')),
    path('school/', include('school.urls')),
    path('api/auth/', include('users.urls')),
    path('api/modules/', include('modules.urls')),
    path('api/simulations/', include('simulations.urls')),
    path('api/ai/', include('ai_service.urls')),
    path('api/gamification/', include('gamification.urls')),
    path('api/social/', include('social.urls')),
    path('dashboard/', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
