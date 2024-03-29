# Generated by Django 4.1.7 on 2023-03-27 09:59

import django.contrib.postgres.fields.citext
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("estat", "0004_importfromconfigtask_task_verbosity"),
    ]

    operations = [
        migrations.CreateModel(
            name="ImportConfigTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "code",
                    django.contrib.postgres.fields.citext.CICharField(
                        max_length=60, unique=True
                    ),
                ),
            ],
        ),
        migrations.AlterModelOptions(
            name="importfromconfigtask",
            options={
                "get_latest_by": "created_on",
                "verbose_name": "Import config result",
                "verbose_name_plural": "Import configs results",
            },
        ),
        migrations.AddField(
            model_name="importconfig",
            name="tags",
            field=models.ManyToManyField(
                blank=True,
                help_text="Assigned tags used for filtering and searching; has no impact on the data import",
                to="estat.importconfigtag",
            ),
        ),
    ]
