# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-28 18:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_teacher_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='tag',
            field=models.CharField(default='名校', max_length=10, verbose_name='机构标签'),
        ),
    ]
