# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 12:23
from __future__ import unicode_literals

from django.db import migrations
import fernet_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0004_auto_20170903_1729'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='contact_mob',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='contact_res',
        ),
        migrations.AlterField(
            model_name='teacher',
            name='designation',
            field=fernet_fields.fields.EncryptedTextField(),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='email',
            field=fernet_fields.fields.EncryptedEmailField(max_length=254),
        ),
    ]
