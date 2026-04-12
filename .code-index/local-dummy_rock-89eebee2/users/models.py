from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Days before expiry to start showing the renewal warning popup
SUBSCRIPTION_WARNING_DAYS = 3
# Days after expiry where the dashboard is still accessible (grace period)
SUBSCRIPTION_GRACE_DAYS = 2


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('learner', 'Learner'),
        ('pro', 'Pro'),
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('school_admin', 'School Admin'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='learner')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # School-related fields (Phase 2)
    school = models.ForeignKey(
        'school.School', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='members'
    )
    grade = models.CharField(max_length=5, blank=True, help_text='Student grade level, e.g. 10')
    phone = models.CharField(max_length=15, blank=True)
    # Individual subscription (for pro users not tied to a school)
    subscription_end = models.DateField(
        null=True, blank=True,
        help_text='Subscription expiry date for individual pro users'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def effective_subscription_end(self):
        """
        Returns the relevant subscription end date for this user.
        - admin / superuser: None (never expires)
        - school user: school's subscription_end
        - individual pro: user's own subscription_end
        - free learner with no school: None (open access)
        """
        if self.is_superuser or self.role == 'admin':
            return None
        if self.school_id:
            school = getattr(self, '_cached_school', None) or self.school
            return getattr(school, 'subscription_end', None)
        return self.subscription_end

    @property
    def subscription_days_remaining(self):
        """Days until expiry. Negative = already expired. None = no expiry."""
        end = self.effective_subscription_end
        if end is None:
            return None
        return (end - timezone.now().date()).days

    @property
    def subscription_status(self):
        """
        Returns one of:
          'active'  — subscription is valid, more than 3 days left
          'warning' — expiring within 3 days (show renewal popup)
          'grace'   — expired but within 2-day grace period (show urgent popup)
          'expired' — beyond grace period (block dashboard access)
        """
        if self.is_superuser or self.role == 'admin':
            return 'active'
        days = self.subscription_days_remaining
        if days is None:
            return 'active'
        if days > SUBSCRIPTION_WARNING_DAYS:
            return 'active'
        if days >= 0:
            return 'warning'
        if days >= -SUBSCRIPTION_GRACE_DAYS:
            return 'grace'
        return 'expired'
