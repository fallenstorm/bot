from __future__ import unicode_literals
from django.utils import timezone

from django.db import models

# Create your models here.


class TgGroup(models.Model):
    id = models.IntegerField('Group ID', db_index=True, unique=True, primary_key=True)
    title = models.CharField('Group title', max_length=4000, null=True, blank=True)

    def __str__(self):
        return self.title


class TgUser(models.Model):
    id = models.IntegerField('User ID', db_index=True, unique=True, primary_key=True)
    first_name = models.CharField('First name', max_length=4000, null=True, blank=True)
    last_name = models.CharField('Last name', max_length=4000, null=True, blank=True)
    username = models.CharField('Username', max_length=4000, null=True, blank=True)
    groups = models.ManyToManyField('TgGroup', verbose_name=u'User`s groups', through="UserGroupModel")

    def __str__(self):
        return self.username


class UserGroupModel(models.Model):
    user = models.ForeignKey('TgUser', on_delete=models.CASCADE)
    group = models.ForeignKey('TgGroup', on_delete=models.CASCADE)
    detection_datetime = models.DateTimeField(u'Detection datetime', default=timezone.now)

    class Meta:
        unique_together = (
            ['user', 'group']
        )
