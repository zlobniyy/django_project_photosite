# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodel',
            name='image',
            field=models.ImageField(upload_to='upload/'),
        ),
    ]
