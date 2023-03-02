# Generated by Django 4.1.7 on 2023-03-02 10:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("estat", "0003_remove_importconfig_last_import_time_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="importfromconfigtask",
            name="task_verbosity",
            field=models.PositiveIntegerField(
                choices=[(0, "NONE"), (1, "WARNING"), (2, "INFO"), (3, "DEBUG")],
                default=2,
            ),
        ),
    ]
