# Generated by Django 2.0 on 2018-01-27 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbook_backend', '0003_scenerecording_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenerecording',
            name='duration',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
