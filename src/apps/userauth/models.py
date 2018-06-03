from annoying.fields import AutoOneToOneField
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


def get_ids_from_users(*users):
    return [user.pk if isinstance(user, User) else int(user) for user in users]


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


class UserFriendShipManager(models.Manager):
    def are_friends(self, user1, user2):
        user1_id, user2_id = get_ids_from_users(user1, user2)
        return self.filter(pk=user1_id, friends__pk=user2_id).exists()

    def add(self, user1, user2):
        user1_id, user2_id = get_ids_from_users(user1, user2)
        if user1_id == user2_id:
            raise ValueError(_('You can not add yourself as a friend'))
        if not self.are_friends(user1_id, user2_id):
            through_model = self.model.friends.through
            through_model.objects.bulk_create([
                through_model(from_user_id=user1_id, to_user_id=user2_id),
                through_model(from_user_id=user2_id, to_user_id=user1_id),
            ])
            return True

    def delete(self, user1, user2):
        user1_id, user2_id = get_ids_from_users(user1, user2)
        if self.are_friends(user1_id, user2_id):
            through_model = self.model.friends.through
            through_model.objects.filter(
                Q(from_user_id=user1_id, to_user_id=user2_id) | Q(from_user_id=user2_id, to_user_id=user1_id)
            ).delete()
            return True


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
    friendship = UserFriendShipManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name if self.first_name else "User don't have name"

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UserInfo(models.Model):
    user = AutoOneToOneField(User, primary_key=True, on_delete=models.DO_NOTHING, related_name='info')
    facebook = models.CharField(_('facebook'), max_length=128, blank=True)
    google = models.CharField(_('google'), max_length=128, blank=True)
    deezer = models.CharField(_('deezer'), max_length=128, blank=True)

    class Meta:
        db_table = 'user_info'
        verbose_name = _('user info')
        verbose_name_plural = _('users info')


class FriendInviteManager(models.Manager):
    def is_pending(self, from_user, to_user):
        from_user_id, to_user_id = get_ids_from_users(from_user, to_user)
        return self.filter(from_user_id=from_user_id, to_user_id=to_user_id).exists()

    def add(self, from_user, to_user):
        from_user_id, to_user_id = get_ids_from_users(from_user, to_user)
        if from_user_id == to_user_id:
            raise ValueError(_('You can not add yourself as a friend.'))
        if User.friendship.are_friends(from_user_id, to_user_id):
            raise ValueError(_('You are already friends.'))
        if self.is_pending(from_user_id, to_user_id):
            raise ValueError(_('The application has already been created and is pending.'))
        if self.is_pending(to_user_id, from_user_id):
            User.friendship.add(from_user_id, to_user_id)
            return 2
        self.create(from_user_id=from_user_id, to_user_id=to_user_id)
        return 1

    def approve(self, from_user, to_user):
        from_user_id, to_user_id = get_ids_from_users(from_user, to_user)
        if not self.is_pending(from_user_id, to_user_id):
            raise ValueError(_('The application does not exist.'))
        return User.friendship.add(from_user, to_user)

    def reject(self, from_user, to_user):
        from_user_id, to_user_id = get_ids_from_users(from_user, to_user)
        self.filter(from_user_id=from_user_id, to_user_id=to_user_id).delete()


class FriendInvite(models.Model):
    from_user = models.ForeignKey(User, related_name='out_friend_invites', on_delete=models.DO_NOTHING)
    to_user = models.ForeignKey(User, related_name='in_friend_invites', on_delete=models.DO_NOTHING)

    objects = FriendInviteManager()

    class Meta:
        unique_together = ('from_user', 'to_user')
