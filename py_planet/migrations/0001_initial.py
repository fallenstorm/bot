# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-23 13:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TgGroup',
            fields=[
                ('id', models.IntegerField(db_index=True, primary_key=True, serialize=False, unique=True, verbose_name='Group ID')),
                ('title', models.CharField(blank=True, max_length=4000, null=True, verbose_name='Group title')),
            ],
        ),
        migrations.CreateModel(
            name='TgUser',
            fields=[
                ('id', models.IntegerField(db_index=True, primary_key=True, serialize=False, unique=True, verbose_name='User ID')),
                ('first_name', models.CharField(blank=True, max_length=4000, null=True, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=4000, null=True, verbose_name='Last name')),
                ('username', models.CharField(blank=True, max_length=4000, null=True, verbose_name='Username')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroupModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detection_datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Detection datetime')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='py_planet.TgGroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='py_planet.TgUser')),
            ],
        ),
        migrations.AddField(
            model_name='tguser',
            name='groups',
            field=models.ManyToManyField(through='py_planet.UserGroupModel', to='py_planet.TgGroup', verbose_name='User`s groups'),
        ),
        migrations.AlterIndexTogether(
            name='usergroupmodel',
            index_together=set([('user', 'group')]),
        ),
    ]
