# Generated by Django 2.0 on 2018-06-05 23:23

import bbook_backend.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbook_backend', '0005_auto_20180402_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='title',
            field=models.FileField(blank=True, null=True, storage=bbook_backend.storage_backends.StoryTitleStorage(), upload_to=''),
        ),
    ]
