from annoying.fields import AutoOneToOneField
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email, and password.
        """
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_NONE = 0
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_OTHER = 3
    GENDER_CHOICES = (
        (GENDER_NONE, _('------')),
        (GENDER_MALE, _('Male')),
        (GENDER_FEMALE, _('Female')),
        (GENDER_OTHER, _('Other')),
    )

    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('name'), max_length=100, blank=True)
    last_name = models.CharField(_('surname'), max_length=100, blank=True)
    gender = models.PositiveSmallIntegerField(_('gender'), choices=GENDER_CHOICES, default=GENDER_NONE)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin ' 'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name if self.first_name else 'User dont have name'

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UserInfo(models.Model):
    user = AutoOneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='info')
    facebook = models.CharField(_('facebook'), max_length=128, blank=True)
    google = models.CharField(_('google'), max_length=128, blank=True)
    deezer = models.CharField(_('deezer'), max_length=128, blank=True)

    class Meta:
        db_table = 'user_info'
        verbose_name = _('user info')
        verbose_name_plural = _('users info')
