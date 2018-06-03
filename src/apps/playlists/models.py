from django.db import models
from django.utils.translation import ugettext_lazy as _
from ..songs.models import Song
from ..userauth.models import User


class Playlist(models.Model):
    PUBLIC = 0
    PRIVATE = 1

    name = models.CharField(_('name'), max_length=50)
    management = models.BooleanField(_('management'), default=PUBLIC)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='playlist')
    data_created = models.DateTimeField(_('data created'), auto_now=True)
    vote_time = models.ForeignKey('VoteTime', blank=True, null=True, on_delete=models.DO_NOTHING)
    songs = models.ManyToManyField(Song, blank=True, null=True)

    class Meta:
        verbose_name = _('playlist')
        verbose_name_plural = _('playlist')
        ordering = ('name',)

    def __str__(self):
        return '{}'.format(self.name)


class Vote(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.DO_NOTHING)
    song = models.ForeignKey(Song, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    like = models.BooleanField(_('like'), default=0)


class VoteTime(models.Model):
    begin = models.DateTimeField(_('begin'))
    final = models.DateTimeField(_('final'))
