# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2022-09-02 09:17
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('web', '0005_auto_20220823_1138'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wiki',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('content', models.TextField(verbose_name='内容')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                             related_name='children', to='web.Wiki', verbose_name='父级文章')),
                ('project',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Project', verbose_name='项目')),
            ],
        ),
    ]
