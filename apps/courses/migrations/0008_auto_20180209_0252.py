# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-09 02:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_lesson_learn_times'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='learn_times',
        ),
        migrations.AddField(
            model_name='video',
            name='learn_times',
            field=models.IntegerField(default=0, verbose_name='学习时长(分钟数)'),
        ),
    ]
