# Generated by Django 2.0 on 2018-06-26 20:54

import bbook_backend.storage_backends
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbook_backend', '0006_story_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='recording',
            field=models.FileField(blank=True, null=True, storage=bbook_backend.storage_backends.StoryStorage(), upload_to=''),
        ),
        migrations.AddField(
            model_name='story',
            name='scene_durations',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='story',
            name='scenes',
            field=models.ManyToManyField(related_name='stories', to='bbook_backend.Scene'),
        ),
    ]
