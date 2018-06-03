from django.db import models
from django.utils.translation import ugettext_lazy as _
from ..songs.models import Song
from ..userauth.models import User


class Playlist(models.Model):
    PUBLIC = 0
    PRIVATE = 1

    name = models.CharField(_('name'), max_length=255, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlist')
    is_public = models.BooleanField(_('management'), default=PUBLIC, db_index=True)
    vote_time = models.OneToOneField('VoteTime', blank=True, null=True, on_delete=models.DO_NOTHING)
    data_created = models.DateTimeField(_('data created'), auto_now=True)

    class Meta:
        verbose_name = _('playlist')
        verbose_name_plural = _('playlist')
        ordering = ('name',)

    def __str__(self):
        return self.name


class PlayManager(models.Manager):
    def create(self, playlist, song, **kwargs):
        if not isinstance(playlist, Playlist) or not isinstance(song, Song):
            raise TypeError
        if Vote.objects.filter(playlist=playlist, song=song).exists():
            kwargs['song_likes'] = Vote.objects.filter(playlist=playlist, song=song).count()
        return super().self.create(playlist=playlist, song=song, **kwargs)


class PlaylistPlay(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.DO_NOTHING)
    song = models.ForeignKey(Song, on_delete=models.DO_NOTHING)
    song_likes = models.PositiveIntegerField(_('count song'), default=0)

    objects = PlayManager()

    class Meta:
        unique_together = ('playlist', 'song')


class Vote(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.DO_NOTHING)
    song = models.ForeignKey(Song, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('playlist', 'song')


class VoteTime(models.Model):
    begin = models.DateTimeField(_('begin'))
    final = models.DateTimeField(_('final'))


class MusicalPreference(models.Model):
    name = models.SlugField(_('slug name'))
