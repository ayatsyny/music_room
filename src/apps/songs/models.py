from django.db import models
from django.utils.translation import ugettext_lazy as _


class AuthorSongManager(models.Manager):
    def create(self, origin_name, **kwargs):
        name = origin_name.strip().lower()
        return super().create(name=name, origin_name=origin_name, **kwargs)


class AuthorSong(models.Model):
    name = models.CharField(_('name'), max_length=255, unique=True)
    origin_name = models.CharField(_('origin name'), max_length=255)

    objects = AuthorSongManager()

    class Meta:
        ordering = ('name',)

    def get_name_db(self):
        return self.name

    def __str__(self):
        return self.origin_name


class Song(models.Model):
    id = models.PositiveIntegerField(_('id'), primary_key=True)
    name = models.CharField(_('name'), max_length=150)
    authors = models.ManyToManyField(AuthorSong, related_name='songs', null=False)
