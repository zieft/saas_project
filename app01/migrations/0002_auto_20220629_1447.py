# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2022-06-29 14:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='phone',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='mobile_phone',
            field=models.CharField(default=1, max_length=12, verbose_name='电话'),
            preserve_default=False,
        ),
    ]
