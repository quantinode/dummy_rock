from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role', 'school', 'subscription_end', 'subscription_status', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'username')
    readonly_fields = ('subscription_status', 'subscription_days_remaining')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Profile', {'fields': ('role', 'bio', 'avatar', 'phone', 'grade', 'school')}),
        ('Subscription', {'fields': ('subscription_end', 'subscription_status', 'subscription_days_remaining')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
