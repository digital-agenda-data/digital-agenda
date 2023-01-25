# Generated by Django 4.1.4 on 2023-01-25 15:56

import digital_agenda.apps.estat.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("estat", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="importconfig",
            name="filters",
            field=models.JSONField(
                blank=True,
                default=dict,
                help_text="Object with ESTAT dimension keys and an Array of accepted codes as values.",
            ),
        ),
        migrations.RemoveField(
            model_name="importconfig",
            name="last_import_time"
        ),
        migrations.AddField(
            model_name="importconfig",
            name="last_import_time",
            field=models.DateTimeField(
                help_text="Time when the last import was completed, regardless if it was successful or not.",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="importconfig",
            name="mappings",
            field=models.JSONField(
                blank=True,
                default=digital_agenda.apps.estat.models.default_mappings,
                help_text="Define how ESTAT codes are transformed before inserting into the DB",
            ),
        ),
        migrations.AlterField(
            model_name="importconfig",
            name="status",
            field=models.TextField(
                help_text="Status of the import from config task or the error message if it failed"
            ),
        ),
        migrations.AlterField(
            model_name="importconfig",
            name="title",
            field=models.CharField(
                blank=True,
                help_text="Human readable title for logging and differentiating from multiple configs for the same dataset",
                max_length=1024,
                null=True,
            ),
        ),
    ]
