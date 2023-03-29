# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2023-03-29 10:17
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('web', '0012_issuestype_module'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=80, verbose_name='主题')),
                ('desc', models.TextField(verbose_name='问题描述')),
                ('priority',
                 models.CharField(choices=[('danger', '高'), ('warning', '中'), ('success', '低')], default='danger',
                                  max_length=12, verbose_name='优先级')),
                ('status', models.SmallIntegerField(
                    choices=[(1, '新建'), (2, '处理中'), (3, '已解决'), (4, '已忽略'), (5, '待反馈'), (6, '已关闭'),
                             (7, '重新打开')], default=1, verbose_name='状态')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='开始时间')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='结束时间')),
                ('mode',
                 models.SmallIntegerField(choices=[(1, '公开模式'), (2, '隐私模式')], default=1, verbose_name='模式')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('latest_update_datetime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('assign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                             related_name='task', to='web.UserInfo', verbose_name='指派')),
                ('attention',
                 models.ManyToManyField(blank=True, related_name='observe', to='web.UserInfo', verbose_name='关注者')),
                ('creator',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='create_problems',
                                   to='web.UserInfo', verbose_name='创建者')),
                ('issues_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.IssuesType',
                                                  verbose_name='问题类型')),
                ('module',
                 models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Module',
                                   verbose_name='模块')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                             related_name='child', to='web.Issues', verbose_name='父问题')),
                ('project',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Project', verbose_name='项目')),
            ],
        ),
    ]
