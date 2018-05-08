from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    SEX_NONE = 0
    SEX_MALE = 1
    SEX_FEMALE = 2
    SEX_CHOICES = (
        (SEX_NONE, '-------'),
        (SEX_MALE, 'men'),
        (SEX_FEMALE, 'women'),
    )
    email = models.EmailField(_('email'), unique=True)
    login = models.CharField(_('login'), max_length=50)
    first_name = models.CharField(_('name'), max_length=30)
    last_name = models.CharField(_('surname'), max_length=30, blank=True)
    sex = models.SmallIntegerField(_('sex'), choices=SEX_CHOICES, default=SEX_NONE)
    birth_date = models.DateField(_('birthday'), null=True, blank=True)
    city = models.CharField(_('city'), max_length=80, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin ' 'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['login']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('first_name', 'last_name')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
