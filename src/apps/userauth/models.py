from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):

    def _create_user(self, email, login, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email, login and password.
        """
        now = timezone.now()
        email = self.normalize_email(email)
        if not login or (isinstance(login, str) and not login.split()):
            login = email.split('@')[0]
        user = self.model(email=email, login=login, is_staff=is_staff, is_active=True, is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        if self.model.objects.filter(login=login).exists():
            user.login = '{}{}'.format(login, user.pk)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, login, password=None, **extra_fields):
        return self._create_user(email, login, password, False, False, **extra_fields)

    def create_superuser(self, email, login, password, **extra_fields):
        return self._create_user(email, login, password, True, True, **extra_fields)


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
    login = models.CharField(_('login'), max_length=50, unique=True)
    first_name = models.CharField(_('name'), max_length=30, blank=True)
    last_name = models.CharField(_('surname'), max_length=30, blank=True)
    gender = models.PositiveSmallIntegerField(_('gender'), choices=GENDER_CHOICES, default=GENDER_NONE)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin ' 'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('login',)

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('login',)

    def get_full_name(self):
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name if self.first_name else self.login

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Service(models.Model):
    name = models.CharField(_('name'), max_length=255)


class AtachService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='atach_services')
    id_user_service = models.CharField(_('id user service'), max_length=255)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='+')
