# Generated by Django 2.0 on 2017-12-31 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbook_backend', '0002_scenerecording_scene'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenerecording',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
